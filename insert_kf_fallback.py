# -*- coding: utf-8 -*-
"""为站点所有HTML文件在</body>前插入自绘客服悬浮按钮（保留行尾，幂等）。"""
import os
import glob
import sys

EMBED_MARK = "kf-fallback"
KF_LINK = "https://tb.53kf.com/code/client/27ec1d7c4b214323ffe2b58a9848bb6a3/1"

SNIPPET_LF = (
    '\n<!-- 在线客服悬浮按钮（53kf兜底，纯CSS不依赖第三方脚本） -->\n'
    '<style>\n'
    '.kf-fallback{position:fixed;right:20px;bottom:24px;z-index:9998;display:flex;align-items:center;gap:8px;'
    'background:linear-gradient(135deg,#c0392b,#a93226);color:#fff;padding:12px 18px;border-radius:40px;'
    'font-size:14px;font-weight:600;box-shadow:0 6px 18px rgba(192,57,43,.35);cursor:pointer;text-decoration:none;'
    "font-family:'Noto Sans SC',system-ui,sans-serif;transition:transform .2s}\n"
    '.kf-fallback:hover{transform:translateY(-2px)}\n'
    '.kf-fallback svg{width:20px;height:20px;stroke:#fff;fill:none;stroke-width:2}\n'
    '@media(max-width:560px){.kf-fallback{bottom:16px;right:14px;padding:10px 14px;font-size:13px}}\n'
    '</style>\n'
    '<a class="kf-fallback" href="' + KF_LINK + '" target="_blank" rel="noopener">\n'
    '<svg viewBox="0 0 24 24"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>\n'
    '<span>在线客服</span>\n'
    '</a>\n'
    '<script>\n'
    '(function(){\n'
    '  var tries=0;\n'
    '  function check(){\n'
    '    var kf=document.getElementById(\'KFLOGO\');\n'
    '    if(kf){ var r=kf.getBoundingClientRect(); if(r.width>0&&r.height>0){ var b=document.querySelector(\'.kf-fallback\'); if(b)b.style.display=\'none\'; return true; } }\n'
    '    return false;\n'
    '  }\n'
    '  var t=setInterval(function(){ tries++; if(check()||tries>12) clearInterval(t); },500);\n'
    '})();\n'
    '</script>\n'
)


def main(root):
    files = glob.glob(os.path.join(root, "**", "*.html"), recursive=True)
    snippet_crlf = SNIPPET_LF.replace('\n', '\r\n')
    modified = 0
    skipped_existing = 0
    errors = []

    for f in files:
        try:
            with open(f, "r", encoding="utf-8", newline="") as fh:
                content = fh.read()
        except UnicodeDecodeError:
            errors.append("{} : 非UTF-8，跳过".format(os.path.relpath(f, root)))
            continue

        if EMBED_MARK in content:
            skipped_existing += 1
            continue

        if "</body>" not in content:
            errors.append("{} : 无</body>，跳过".format(os.path.relpath(f, root)))
            continue

        snippet = snippet_crlf if content.count("\r\n") > content.count("\n") / 2 else SNIPPET_LF
        new_content = content.replace("</body>", snippet + "</body>", 1)
        with open(f, "w", encoding="utf-8", newline="") as fh:
            fh.write(new_content)
        modified += 1

    print("共发现HTML文件: {}".format(len(files)))
    print("已插入: {}".format(modified))
    print("已存在跳过: {}".format(skipped_existing))
    for e in errors:
        print("错误: " + e)
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python insert_kf_fallback.py <网站根目录>")
        sys.exit(1)
    root = sys.argv[1]
    if not os.path.isdir(root):
        print("错误: 目录不存在: {}".format(root))
        sys.exit(1)
    main(root)
