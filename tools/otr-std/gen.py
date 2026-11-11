#!/usr/bin/env python3
"""Builds the otr standard library reference under otr/std/ from `otr doc`.

    tools/otr-std/gen.py --std ~/otr/src/std

Each module of the standard library becomes one page. A module's page embeds
tools/otr-std/examples/std.<module>.otr and its recorded output when they exist.
The script also rewrites the "Standard library" navigation group in docs.json.
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = Path(__file__).resolve().parent / "examples"
OUT = ROOT / "otr" / "std"
GUIDE = "otr/standard-library"

# Navigation groups, in order. A module missing from here fails the build, so a
# new module of the library cannot be left out of the navigation by accident.
GROUPS = [
    ("Core", ["std", "runtime", "io", "fmt", "log", "debug", "testing", "testing_allocator"]),
    ("Memory", ["mem", "arena", "box", "rc", "arc", "cell", "pool"]),
    ("Collections", ["list", "soa_list", "hash_map", "btree", "deque", "priority_queue",
                     "bitset", "bounded", "sort", "enums"]),
    ("Text and encoding", ["string", "utf8", "ascii", "base64", "json", "uri", "dtoa", "ryu"]),
    ("Files and processes", ["fs", "path", "process", "xdg"]),
    ("Concurrency", ["sync", "thread", "callback"]),
    ("Time", ["time", "datetime", "tz"]),
    ("Math and hashing", ["math", "math.f32_impl", "rand", "hash"]),
    ("Networking", ["net", "socket_stream", "socket_ancillary", "http", "http.parser",
                    "http.url", "tls", "tls.client", "tls.hello", "tls.keys", "tls.peer",
                    "tls.record", "tls.wire"]),
    ("Cryptography", ["crypto", "crypto.sha2", "crypto.md5", "crypto.hmac", "crypto.hkdf",
                      "crypto.aes", "crypto.aes_gcm", "crypto.aes_ccm", "crypto.aes_cmac",
                      "crypto.chacha20poly1305", "crypto.x25519", "crypto.ed25519",
                      "crypto.field25519", "crypto.ecc", "crypto.ecdsa", "crypto.rsa",
                      "crypto.bigint", "crypto.asn1", "crypto.x509", "crypto.ca_bundle",
                      "crypto.hostname"]),
    ("Compression", ["flate", "flate_common", "flate_deflate", "flate_inflate",
                     "flate_match", "flate_tree"]),
    ("Linux", ["linux", "linux.fd", "linux.mapping", "linux.metadata", "linux.process"]),
    ("C interop", ["ffi", "ffi_context", "cstr", "dl"]),
]

# Top-level section names by module, for links from one module's re-exports to another.
HEADINGS = {}

FALLBACK_INTRO = {"math.f32_impl": "`exp`, `log` and `pow` for `f32`."}

HEADING = re.compile(r"^(#{1,4}) `(.*)`\s*$")
TYPE_KINDS = ("struct", "ref struct", "packed struct", "extern struct", "enum", "union",
              "interface", "error")


class Item:
    def __init__(self, level, sig):
        self.level = level
        self.sig = sig
        self.doc = []
        self.children = []

    @property
    def is_fn(self):
        return re.match(r"^((pub|unsafe|simd|inline|export|extern) )*fn ", self.sig) is not None

    @property
    def is_const(self):
        return self.sig.startswith("const ")

    @property
    def name(self):
        if self.is_fn:
            return re.search(r"fn ([A-Za-z_0-9]+)", self.sig).group(1)
        if self.is_const:
            return re.match(r"const ([A-Za-z_0-9]+)", self.sig).group(1)
        return re.match(r"[A-Za-z_0-9]+", self.sig).group(0)

    @property
    def is_member(self):
        """A struct field or an enum or union variant."""
        return not self.is_fn and not self.is_const

    @property
    def value(self):
        return self.sig.split(" = ", 1)[1] if " = " in self.sig else ""

    @property
    def is_type(self):
        if self.is_fn:
            return self.sig.endswith(") type")
        return self.is_const and (self.value in TYPE_KINDS or self.value.startswith("error {")
                                  or bool(self.children))

    def text(self):
        return "\n".join(self.doc).strip("\n")


def parse(markdown):
    """The module's own doc text and its top-level items."""
    stack, top, intro = [], [], []
    for line in markdown.splitlines():
        m = HEADING.match(line)
        if not m:
            (stack[-1].doc if stack else intro).append(line)
            continue
        level = len(m.group(1))
        if level == 1:
            continue
        item = Item(level, m.group(2))
        while stack and stack[-1].level >= level:
            stack.pop()
        (stack[-1].children if stack else top).append(item)
        stack.append(item)
    return "\n".join(intro).strip("\n"), top


def escape_prose(text):
    """Makes doc-comment text safe as MDX: fences its code, escapes the rest."""
    out, code, para = [], [], []

    def flush_para():
        if para:
            joined = "\n".join(para)
            parts = re.split(r"(`[^`]*`)", joined)
            for i in range(0, len(parts), 2):
                parts[i] = (parts[i].replace("{", "\\{").replace("}", "\\}")
                            .replace("<", "&lt;").replace("–", "-"))
            out.append("".join(parts))
            para.clear()

    def flush_code():
        while code and not code[-1].strip():
            code.pop()
        if code:
            out.append("```otr\n" + "\n".join(line[4:] for line in code) + "\n```")
            code.clear()

    for line in text.splitlines():
        if line.startswith("    ") and (code or not para):
            code.append(line)
        elif not line.strip():
            if code:
                code.append(line)
            else:
                flush_para()
        else:
            flush_code()
            para.append(line)
    flush_code()
    flush_para()
    return "\n\n".join(out)


def one_line(text):
    return re.sub(r"\s+", " ", escape_prose(text)).strip()


def code_cell(text):
    """Inline code for a table cell. Backticks cannot hold an escaped pipe."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace("{", "&#123;")
    return "<code>" + text.replace("}", "&#125;").replace("|", "\\|") + "</code>"


def table(header, rows):
    lines = ["| " + " | ".join(header) + " |", "|" + " --- |" * len(header)]
    lines += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(lines)


CONTAINER = re.compile(r"^pub const (\w+) = (?:(?:ref|extern|packed) )?(?:struct|error|enum|union)\b.*\{$")
TYPE_FN = re.compile(r"^(?:pub )?(?:unsafe )?fn (\w+)\(.*\) type \{$")
FIELD = re.compile(r"^(pub )?([a-z_]\w*): (.+?),?$")
VARIANT = re.compile(r"^([A-Z]\w*),?$")


def source_members(source):
    """Fields and error names by type name, read from the source.

    `otr doc` leaves out fields that are not `pub`, which other modules can still
    read, and the names of an error set written over several lines.
    """
    found, name, indent, doc, fn = {}, None, 0, [], None
    for line in source.splitlines():
        if name is None:
            m = CONTAINER.match(line)
            if m:
                name, indent, doc = m.group(1), 4, []
            elif TYPE_FN.match(line):
                fn = TYPE_FN.match(line).group(1)
            elif fn and re.match(r"^    return (?:(?:ref|extern|packed) )?struct \{$", line):
                name, indent, doc = fn, 8, []
            continue
        if line == " " * (indent - 4) + "}":
            name = None
            continue
        if not line.startswith(" " * indent) or line[indent:indent + 1] == " ":
            continue
        body = line[indent:]
        if body.startswith("///"):
            doc.append(body[3:].strip())
            continue
        m = FIELD.match(body) or VARIANT.match(body)
        if m and not body.startswith("__"):
            public = m.re is VARIANT or bool(m.group(1))
            sig = body.removeprefix("pub ").rstrip(",")
            found.setdefault(name, []).append((sig, "\n".join(doc), public))
        doc = []
    return found


def delegates(source, name):
    """The type functions `name` returns the result of, when that is all it does."""
    m = re.search(r"^(?:pub )?(?:unsafe )?fn " + name + r"\([^\n]*\) type \{\n(.*?)^\}", source,
                  re.S | re.M)
    return re.findall(r"^\s+return (?:unsafe \{ )?([A-Z]\w*)\(", m.group(1), re.M) if m else []


def balanced(sig):
    return all(sig.count(a) == sig.count(b) for a, b in ("()", "[]", "{}"))


def whole_const(source, name):
    """A constant's full definition, which `otr doc` cuts at the end of its first line."""
    lines = source.splitlines()
    for i, line in enumerate(lines):
        if re.match(r"^\s*(pub )?const " + name + r"\b", line):
            text = line.strip().removeprefix("pub ")
            for more in lines[i + 1:]:
                if balanced(text):
                    break
                text += " " + more.strip()
            return re.sub(r"([(\[]) ", r"\1", re.sub(r" ([)\]])", r"\1", text))
    return None


def mend(items, source):
    for it in items:
        if not balanced(it.sig):
            if it.is_member:
                it.sig = it.sig.split(" = ", 1)[0]
            elif it.is_const:
                it.sig = whole_const(source, it.name) or it.sig
        mend(it.children, source)


def complete(items, shadow, source):
    """Adds what `otr doc` leaves out: unlisted members, and the members of a type
    function that only forwards to another one."""
    mend(items, source)
    mend(shadow, source)
    by_name = {it.name: it for it in shadow}
    hidden = set(by_name) - {it.name for it in items}
    by_name.update({it.name: it for it in items})
    members = source_members(source)

    def fill(it, seen):
        for sig, doc, public in members.get(it.name, []):
            if all(c.name != re.match(r"\w+", sig).group(0) or not c.is_member
                   for c in it.children):
                child = Item(it.level + 1, sig)
                child.doc = doc.splitlines()
                child.read_only = not public
                it.children.append(child)
        if it.is_fn and it.is_type and not it.children:
            targets = [t for t in delegates(source, it.name) if t in by_name and t not in seen]
            if targets:
                target = by_name[targets[-1]]
                fill(target, seen | {it.name})
                it.children = target.children
        if it.is_const and not it.children:
            # A constant that names a type built by a private function.
            for t in re.findall(r"([A-Z]\w*)\(", it.value):
                if t in hidden and by_name[t].is_type:
                    fill(by_name[t], seen | {it.name})
                    it.children = by_name[t].children

    for it in list(by_name.values()):
        fill(it, set())


def member_table(members):
    members = sorted(members, key=lambda m: getattr(m, "read_only", False))
    typed = [":" in m.sig for m in members]
    private = [getattr(m, "read_only", False) for m in members]
    header = ["Variant"] if not any(typed) else ["Field" if all(typed) else "Member", "Type"]
    rows = []
    for m, hidden in zip(members, private):
        name, _, rest = m.sig.partition(": ")
        row = [code_cell(name)]
        if any(typed):
            row.append(code_cell(rest) if rest else "")
        if any(private):
            row.append("Read-only" if hidden else "Public")
        rows.append(row + [one_line(m.text())])
    if any(private):
        header.append("Access")
    if any(r[-1] for r in rows):
        return table(header + ["Description"], rows)
    return table(header, [r[:-1] for r in rows])


def render_items(items, prefix, depth, modules):
    """Sections for `items`, then one table of the constants that need no prose."""
    out, plain = [], []
    for it in items:
        if it.is_member:
            continue
        if it.is_const and not it.is_type and not it.text():
            plain.append(it)
            continue
        title = prefix + it.name
        out.append("#" * depth + " " + title)
        out.append("```otr\n" + it.sig + "\n```")
        if it.text():
            out.append(escape_prose(it.text()))
        members = [c for c in it.children if c.is_member]
        if members:
            out.append(member_table(members))
        if it.children:
            out += render_items(it.children, title + ".", min(depth + 1, 4), modules)
    if plain:
        if not prefix:
            out.append("## Constants")
        rows = [[code_cell(prefix + c.name), link_value(c.value, modules)] for c in plain]
        out.append(table(["Name", "Definition"], rows))
    return out


def link_value(value, modules):
    """Links `module.name` to that module's page when it is a std module."""
    m = re.match(r"^([a-z_0-9]+)\.([A-Za-z_0-9]+)$", value)
    cell = code_cell(value)
    if m:
        target = modules.get(m.group(1))
        if target:
            anchor = "#" + m.group(2).lower() if m.group(2) in HEADINGS.get(target, ()) else ""
            return f"[{cell}](/{page_path(target)}{anchor})"
    return cell


def page_path(module):
    return "otr/std/" + ("std" if module == "std" else module.replace(".", "/"))


def summary(intro, module):
    """The first sentence of the module's doc text, without code formatting."""
    text = re.sub(r"\s+", " ", intro).strip()
    parts = re.split(r"(`[^`]*`)", text)
    first = ""
    for i, part in enumerate(parts):
        if i % 2:
            first += part[1:-1]
            continue
        m = re.search(r"[.:;](\s|$)", part)
        if m:
            first += part[:m.start()]
            break
        first += part
    return (first.strip() + ".") if first.strip() else f"The std.{module} module."


def example_section(module):
    src = EXAMPLES / f"std.{module}.otr"
    if module == "std" or not src.exists():
        return []
    out = ["## Example", "```otr\n" + src.read_text().rstrip("\n") + "\n```"]
    printed = EXAMPLES / f"std.{module}.out"
    if printed.exists() and printed.read_text().strip():
        out.append("```text\n" + printed.read_text().rstrip("\n") + "\n```")
    return out


def source_intro(source):
    """The `///` block that opens a file and ends at a blank line: the module's doc."""
    lines = []
    for line in source.splitlines():
        if line.startswith("///"):
            lines.append(line[3:].removeprefix(" "))
        elif lines or not line.startswith("//"):
            return "\n".join(lines) if lines and not line.strip() else ""
    return ""


def read_page(module, markdown, source, shadow_markdown):
    """The module's doc text and its items, with what `otr doc` leaves out added."""
    intro, items = parse(markdown)
    complete(items, parse(shadow_markdown)[1], source)
    if not intro:
        # `otr doc` gives a module doc that no import follows to the first declaration.
        intro = source_intro(source) or FALLBACK_INTRO.get(module, "")
        if items and items[0].text().startswith(intro):
            items[0].doc = items[0].text()[len(intro):].splitlines()
    HEADINGS[module] = {it.name for it in items if it.is_fn or it.is_type or it.text()}
    return intro, items


def write_page(module, intro, items, modules):
    full = "std" if module == "std" else "std." + module
    desc = summary(intro, module).replace("\\", "\\\\").replace('"', '\\"')
    parts = [f'---\ntitle: "{full}"\nsidebarTitle: "{module}"\ndescription: "{desc}"\n---']
    if intro:
        parts.append(escape_prose(intro))
    parts.append(f"```otr\nimport {full}\n```")
    parts += example_section(module)
    parts += render_items(items, "", 2, modules)
    return "\n\n".join(parts) + "\n", summary(intro, module)


def render_index(summaries):
    parts = ['---\ntitle: "Standard library reference"\nsidebarTitle: "All modules"\n'
             'description: "Every module of the otr standard library, with each public '
             'declaration."\n---',
             "Each page lists a module's public declarations with their signatures and "
             "doc comments, as `otr doc` prints them. For a guided tour with longer "
             f"examples, read the [standard library guide](/{GUIDE}).",
             "Reach a module as `std.<name>` after `import std`, or import it on its "
             "own with `import std.<name>`."]
    for group, mods in GROUPS:
        rows = [[f"[`std.{m}`](/{page_path(m)})" if m != "std" else f"[`std`](/{page_path(m)})",
                 one_line(summaries[m])] for m in mods]
        parts += ["## " + group, table(["Module", "Purpose"], rows)]
    return "\n\n".join(parts) + "\n"


def update_nav(docs_json):
    data = json.loads(docs_json.read_text())
    tab = next(t for t in data["navigation"]["tabs"] if t["tab"] == "otr")
    group = {"group": "Standard library", "pages": [GUIDE, "otr/std/index"] + [
        {"group": name, "pages": [page_path(m) for m in mods]} for name, mods in GROUPS]}
    for g in tab["groups"]:
        g["pages"] = [p for p in g["pages"] if p != GUIDE]
    kept = [g for g in tab["groups"] if g["group"] != "Standard library"]
    at = next(i for i, g in enumerate(kept) if g["group"] == "Reference")
    tab["groups"] = kept[:at] + [group] + kept[at:]
    docs_json.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--std", required=True, type=Path,
                    help="the directory that holds std.otr and std/ (src/std of an otr checkout)")
    ap.add_argument("--otr", default="otr", help="the otr compiler to run")
    args = ap.parse_args()

    files = {}
    for f in sorted(args.std.rglob("*.otr")):
        rel = f.relative_to(args.std).with_suffix("")
        files[".".join(rel.parts[1:]) or "std"] = f
    listed = [m for _, mods in GROUPS for m in mods]
    if sorted(listed) != sorted(files):
        sys.exit(f"GROUPS and {args.std} disagree: "
                 f"{sorted(set(listed) ^ set(files))}")

    # A re-export names its module by the last path segment, as the import binds it.
    modules = {m.rsplit(".", 1)[-1]: m for m in files if m != "std"}
    parsed, summaries = {}, {}
    for module, f in files.items():
        doc = subprocess.run([args.otr, "doc", f.name], cwd=f.parent, check=True,
                             capture_output=True, text=True).stdout
        source = f.read_text()
        # Private type functions, made public so that `otr doc` lists their members
        # for the public functions that return them.
        opened = re.sub(r"^fn ([A-Z]\w*\(.*\) type \{)$", r"pub fn \1", source, flags=re.M)
        shadow = doc
        if opened != source:
            with tempfile.TemporaryDirectory() as tmp:
                (Path(tmp) / f.name).write_text(opened)
                shadow = subprocess.run([args.otr, "doc", f.name], cwd=tmp, check=True,
                                        capture_output=True, text=True).stdout
        parsed[module] = read_page(module, doc, source, shadow)

    for old in OUT.rglob("*.mdx") if OUT.exists() else []:
        old.unlink()
    for module, (intro, items) in parsed.items():
        text, summaries[module] = write_page(module, intro, items, modules)
        path = ROOT / (page_path(module) + ".mdx")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    (OUT / "index.mdx").write_text(render_index(summaries))
    update_nav(ROOT / "docs.json")
    print(f"wrote {len(parsed) + 1} pages to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
