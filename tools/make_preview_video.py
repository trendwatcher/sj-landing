"""VOD 과정 미리보기 영상을 만듭니다.

실제 강의 촬영본이 아니라, 과정 소개를 글자와 움직임으로 보여 주는
'모션 그래픽' 영상입니다. 나중에 진짜 강의 영상이 준비되면
public/videos/ 의 파일만 바꿔 끼우면 됩니다.

실행:  python tools/make_preview_video.py
필요:  Pillow, ffmpeg
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ── 기본 설정 ────────────────────────────────────────────────
W, H = 1280, 720
FPS = 30
OUT_DIR = Path(__file__).resolve().parent.parent / "public" / "videos"

FONT_BOLD = "C:/Windows/Fonts/malgunbd.ttf"
FONT_BASE = "C:/Windows/Fonts/malgun.ttf"

# 홈페이지와 같은 색 (베이지 + 테라코타)
CREAM_TOP = (253, 250, 244)
CREAM_BOTTOM = (244, 235, 218)
INK = (47, 41, 34)
INK_SOFT = (110, 99, 87)
BRAND = (194, 97, 31)
BRAND_DARK = (140, 66, 16)
AMBER = (232, 152, 42)
WHITE = (255, 255, 255)

CONTACT_PHONE = "010-8624-8866"
BRAND_NAME = "김세진 소상공인 컨설팅"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def ease_out(t: float) -> float:
    """0→1 을 부드럽게 (처음 빠르고 끝에서 천천히)."""
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def background() -> Image.Image:
    """위에서 아래로 이어지는 베이지 그라데이션 배경."""
    base = Image.new("RGB", (W, H), CREAM_TOP)
    draw = ImageDraw.Draw(base)
    for y in range(H):
        ratio = y / H
        color = tuple(
            round(CREAM_TOP[i] + (CREAM_BOTTOM[i] - CREAM_TOP[i]) * ratio) for i in range(3)
        )
        draw.line([(0, y), (W, y)], fill=color)

    # 오른쪽 위 은은한 빛무리
    glow = Image.new("RGB", (W, H), CREAM_TOP)
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([W - 460, -240, W + 160, 380], fill=(249, 223, 201))
    return Image.blend(base, glow, 0.35)


def blend_text(
    img: Image.Image,
    xy: tuple[int, int],
    text: str,
    fnt: ImageFont.FreeTypeFont,
    color: tuple[int, int, int],
    alpha: float,
    anchor: str = "la",
) -> None:
    """알파(투명도)를 적용해 글자를 얹습니다."""
    if alpha <= 0.01:
        return
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).text(
        xy, text, font=fnt, fill=color + (round(255 * min(1.0, alpha)),), anchor=anchor
    )
    img.alpha_composite(layer) if img.mode == "RGBA" else img.paste(
        Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB"), (0, 0)
    )


def rounded_bar(img: Image.Image, progress: float) -> None:
    """아래쪽 진행 막대."""
    draw = ImageDraw.Draw(img)
    y = H - 8
    draw.rectangle([0, y, W, H], fill=(233, 220, 196))
    draw.rectangle([0, y, int(W * progress), H], fill=BRAND)


def draw_scene(
    frame_no: int,
    total_frames: int,
    scenes: list[dict],
) -> Image.Image:
    """현재 프레임이 속한 장면을 그립니다."""
    img = background()
    t = frame_no / FPS

    # 머리말 (항상 표시)
    head = font(FONT_BOLD, 26)
    blend_text(img, (64, 52), BRAND_NAME, head, BRAND_DARK, 1.0)
    blend_text(img, (W - 64, 56), "과정 미리보기", font(FONT_BASE, 22), INK_SOFT, 1.0, anchor="ra")

    elapsed = 0.0
    for scene in scenes:
        if elapsed <= t < elapsed + scene["dur"]:
            local = t - elapsed
            draw_lines(img, scene, local)
            break
        elapsed += scene["dur"]

    rounded_bar(img, frame_no / max(1, total_frames - 1))
    return img


def draw_lines(img: Image.Image, scene: dict, local: float) -> None:
    """한 장면 안의 글줄을 차례로 띄웁니다."""
    fade_out = 1.0
    remain = scene["dur"] - local
    if remain < 0.45:
        fade_out = max(0.0, remain / 0.45)

    for line in scene["lines"]:
        delay = line.get("delay", 0.0)
        progress = ease_out((local - delay) / 0.55)
        if progress <= 0:
            continue

        alpha = progress * fade_out
        offset = round((1 - progress) * 26)
        fnt = font(line.get("font", FONT_BASE), line["size"])
        color = line.get("color", INK)
        x = line.get("x", 96)
        anchor = "ma" if line.get("center") else "la"
        if line.get("center"):
            x = W // 2

        if line.get("chip"):
            chip_w = round(fnt.getlength(line["text"])) + 44
            chip_h = line["size"] + 26
            layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
            ImageDraw.Draw(layer).rounded_rectangle(
                [x, line["y"] + offset, x + chip_w, line["y"] + offset + chip_h],
                radius=chip_h // 2,
                fill=BRAND + (round(255 * alpha),),
            )
            img.paste(
                Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB"), (0, 0)
            )
            blend_text(
                img,
                (x + 22, line["y"] + offset + 13),
                line["text"],
                fnt,
                WHITE,
                alpha,
            )
            continue

        blend_text(img, (x, line["y"] + offset), line["text"], fnt, color, alpha, anchor)


def build_scenes(course: dict) -> list[dict]:
    """과정 하나의 장면 구성."""
    b, r = FONT_BOLD, FONT_BASE
    return [
        {
            "dur": 3.6,
            "lines": [
                {"text": course["tag"], "y": 240, "size": 26, "font": b, "chip": True},
                {"text": course["title"], "y": 320, "size": 76, "font": b, "delay": 0.35},
                {
                    "text": course["subtitle"],
                    "y": 430,
                    "size": 30,
                    "color": INK_SOFT,
                    "delay": 0.7,
                },
            ],
        },
        {
            "dur": 4.2,
            "lines": [
                {"text": "이런 분께 필요합니다", "y": 200, "size": 40, "font": b, "color": BRAND_DARK},
                *[
                    {
                        "text": f"· {item}",
                        "y": 300 + i * 66,
                        "size": 32,
                        "delay": 0.4 + i * 0.35,
                    }
                    for i, item in enumerate(course["who"])
                ],
            ],
        },
        {
            "dur": 4.6,
            "lines": [
                {"text": "이렇게 배웁니다", "y": 190, "size": 40, "font": b, "color": BRAND_DARK},
                *[
                    {
                        "text": f"{i + 1}. {item}",
                        "y": 285 + i * 64,
                        "size": 31,
                        "delay": 0.4 + i * 0.32,
                    }
                    for i, item in enumerate(course["curriculum"])
                ],
            ],
        },
        {
            "dur": 3.4,
            "lines": [
                {
                    "text": "지금 바로 들으실 수 있습니다",
                    "y": 250,
                    "size": 46,
                    "font": b,
                    "center": True,
                },
                {
                    "text": "상담 문의",
                    "y": 360,
                    "size": 26,
                    "color": INK_SOFT,
                    "center": True,
                    "delay": 0.4,
                },
                {
                    "text": CONTACT_PHONE,
                    "y": 400,
                    "size": 62,
                    "font": b,
                    "color": BRAND,
                    "center": True,
                    "delay": 0.6,
                },
            ],
        },
    ]


def render(course: dict) -> None:
    scenes = build_scenes(course)
    total_frames = round(sum(s["dur"] for s in scenes) * FPS)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        for i in range(total_frames):
            draw_scene(i, total_frames, scenes).save(tmp_path / f"f{i:05d}.png")

        # 표지 이미지 (영상이 재생되기 전에 보이는 그림)
        draw_scene(round(2.4 * FPS), total_frames, scenes).save(
            OUT_DIR / f"{course['slug']}.jpg", quality=88
        )

        mp4 = OUT_DIR / f"{course['slug']}.mp4"
        subprocess.run(
            [
                "ffmpeg", "-y", "-loglevel", "error",
                "-framerate", str(FPS),
                "-i", str(tmp_path / "f%05d.png"),
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-crf", "26",
                "-movflags", "+faststart",
                str(mp4),
            ],
            check=True,
        )
        size_mb = mp4.stat().st_size / 1024 / 1024
        print(f"  완료: {mp4.name}  ({total_frames / FPS:.1f}초, {size_mb:.2f}MB)")


COURSES = [
    {
        "slug": "item-selection",
        "tag": "창업 준비",
        "title": "아이템 선정 방법",
        "subtitle": "무엇을 팔 것인가부터 정합니다",
        "who": [
            "창업은 하고 싶은데 무엇을 팔지 못 정한 분",
            "아이템은 있는데 될지 확신이 없는 분",
            "남 따라 시작했다가 접어 본 경험이 있는 분",
        ],
        "curriculum": [
            "내 조건 정리하기 — 자본·시간·경험",
            "시장에서 찾기 — 수요가 있는 자리 보는 법",
            "겹쳐 보기 — 내 조건과 시장이 만나는 지점",
            "검증하기 — 크게 벌이기 전에 작게 시험",
        ],
    },
    {
        "slug": "business-plan",
        "tag": "지원사업 · 대출",
        "title": "사업계획서 작성법",
        "subtitle": "심사위원이 무엇을 보는지부터",
        "who": [
            "정부지원사업에 도전하려는 분",
            "서류가 어려워 중간에 포기해 본 분",
            "써 냈지만 계속 떨어지는 분",
        ],
        "curriculum": [
            "심사 기준 읽기 — 배점표부터 확인",
            "문제와 해결 — 왜 이 사업이 필요한가",
            "숫자로 말하기 — 매출 계획과 근거",
            "마무리 점검 — 빠뜨리기 쉬운 항목",
        ],
    },
]


def main() -> int:
    print("VOD 미리보기 영상을 만듭니다…")
    for course in COURSES:
        print(f"- {course['title']}")
        render(course)
    print("끝났습니다. public/videos/ 를 확인하세요.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
