#!/usr/bin/env python3
"""Replace broken JPG stubs and missing AVIF paths with working Pinerolo assets."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://casafamigliaquercia.it"
PIN = "/images/Pinerolo%20-%20Casa%20Famiglia%20Quercia%201"
DINING = "/images/Sala%20da%20Pranzo%20%2B%20persone%201.avif"
OG_IMAGE = f"{SITE}{DINING}"

# Legacy descriptive filenames → imgN.avif (only img1–img12 exist on disk)
LEGACY_TO_IMG = {
    "Cucina 1.avif": "img6.avif",
    "Ingresso 2.avif": "img2.avif",
    "Esterno 1.avif": "img9.avif",
    "Esterno 3.avif": "img10.avif",
    "Sala da Pranzo + persone 1.avif": "../Sala da Pranzo + persone 1.avif",  # at images/ root
    "Sala da Pranzo + persone 2.avif": "img11.avif",
    "Salone 1.avif": "img1.avif",
    "Camera 1.avif": "img7.avif",
    "Camera 9.avif": "img8.avif",
    "Spazi Comuni.avif": "img3.avif",
}

GLOBAL_REPLACEMENTS = [
    ("https://casafamigliaquercia.it/images/map-placeholder.jpg", OG_IMAGE),
    (f"{PIN}/Sala%20da%20Pranzo%20%2B%20persone%201.avif", DINING),
    ("../images/map-placeholder.jpg", f"{PIN}/img4.avif"),
    ("../../images/map-placeholder.jpg", f"{PIN}/img3.avif"),
    ("../images/avatars/avatar1.jpg", f"{PIN}/img6.avif"),
    ("../images/avatars/avatar2.jpg", f"{PIN}/img7.avif"),
    ("../images/avatars/avatar3.jpg", f"{PIN}/img8.avif"),
]

PAGE_IMG = {
    "servizi/index.html": [
        ("../images/avatars/avatar2.jpg", f"{PIN}/img2.avif"),
    ],
    "la-giornata/index.html": [
        ("../images/avatars/avatar1.jpg", DINING),
    ],
    "rette-e-ammissione/index.html": [
        ("../images/map-placeholder.jpg", f"{PIN}/img3.avif"),
    ],
    "contatti/index.html": [
        ("../images/map-placeholder.jpg", f"{PIN}/img4.avif"),
    ],
    "chi-siamo/index.html": [
        ("../images/map-placeholder.jpg", f"{PIN}/img5.avif"),
    ],
    "storia/index.html": [
        ("../images/map-placeholder.jpg", f"{PIN}/img9.avif"),
    ],
    "casa-famiglia-pinerolo/index.html": [
        ("../images/map-placeholder.jpg", DINING),
    ],
    "casa-famiglia-coazze/index.html": [
        ("../images/map-placeholder.jpg", f"{PIN}/img10.avif"),
    ],
    "casa-famiglia-valle-di-susa/index.html": [
        ("../images/avatars/avatar3.jpg", f"{PIN}/img11.avif"),
    ],
    "casa-famiglia-giaveno/index.html": [
        ("../images/avatars/avatar2.jpg", f"{PIN}/img12.avif"),
    ],
    "casa-famiglia-avigliana/index.html": [
        ("../images/avatars/avatar1.jpg", f"{PIN}/img1.avif"),
    ],
    "blog/anziani-autosufficienti-coazze/index.html": [
        ("../../images/map-placeholder.jpg", f"{PIN}/img2.avif"),
    ],
}


def encode_path(raw: str) -> str:
    if raw.startswith("../"):
        # dining room at images root from blog subfolder
        return "/images/Sala%20da%20Pranzo%20%2B%20persone%201.avif"
    if raw.startswith("/"):
        return raw
    return f"{PIN}/{raw}"


def fix_legacy_paths(content: str) -> str:
    for legacy, target in LEGACY_TO_IMG.items():
        encoded_target = encode_path(target)
        patterns = [
            f"../images/Pinerolo - Casa Famiglia Quercia 1/{legacy}",
            f"../../images/Pinerolo - Casa Famiglia Quercia 1/{legacy}",
        ]
        for pat in patterns:
            content = content.replace(pat, encoded_target)
    return content


def normalize_relative_images(content: str) -> str:
    """Convert ../images/… and ../../images/… to root-absolute encoded paths."""
    replacements = [
        # Longer prefixes first to avoid ..//images/ double-slash bug
        ("../../images/Pinerolo - Casa Famiglia Quercia 1/", f"{PIN}/"),
        ("../../images/Pinerolo%20-%20Casa%20Famiglia%20Quercia%201/", f"{PIN}/"),
        ("../../images/Sala da Pranzo + persone 1.avif", DINING),
        ("../../images/Sala%20da%20Pranzo%20%2B%20persone%201.avif", DINING),
        ("../images/Pinerolo - Casa Famiglia Quercia 1/", f"{PIN}/"),
        ("../images/Pinerolo%20-%20Casa%20Famiglia%20Quercia%201/", f"{PIN}/"),
        ("../images/Sala da Pranzo + persone 1.avif", DINING),
        ("../images/Sala%20da%20Pranzo%20%2B%20persone%201.avif", DINING),
        ("..//images/", "/images/"),
    ]
    for old, new in replacements:
        content = content.replace(old, new)
    return content


def process_file(rel: str) -> bool:
    path = ROOT / rel
    if not path.exists():
        return False
    content = path.read_text(encoding="utf-8")
    original = content

    for old, new in GLOBAL_REPLACEMENTS:
        content = content.replace(old, new)

    for old, new in PAGE_IMG.get(rel, []):
        content = content.replace(old, new)

    content = fix_legacy_paths(content)
    content = normalize_relative_images(content)

    if content != original:
        path.write_text(content, encoding="utf-8")
        print(f"OK {rel}")
        return True
    return False


def main() -> None:
    changed = 0
    for html in sorted(ROOT.rglob("*.html")):
        rel = str(html.relative_to(ROOT))
        if process_file(rel):
            changed += 1
    print(f"Updated {changed} files.")


if __name__ == "__main__":
    main()
