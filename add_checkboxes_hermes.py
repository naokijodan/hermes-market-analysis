#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
エルメスHTMLにチェックボックス機能を追加するスクリプト
"""

import re

# HTMLファイルを読み込む
with open('/Users/naokijodan/Desktop/リサーチファイル/HERMES_市場分析_統合版_2026-01-23.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# チェックボックス用のCSSを追加
checkbox_css = '''
        .search-checkbox {
            margin-left: 5px;
            margin-right: 10px;
            cursor: pointer;
            width: 16px;
            height: 16px;
            vertical-align: middle;
        }
'''

# CSSの .search-link:hover の後に挿入
css_insertion_pattern = r'(\.search-link:hover \{[^}]+\})'
html_content = re.sub(
    css_insertion_pattern,
    r'\1' + '\n' + checkbox_css,
    html_content,
    count=1
)

# チェックボックス用のJavaScript（localStorage管理）を追加
checkbox_js = '''
        // チェックボックスのlocalStorage管理
        function initCheckboxes() {
            document.addEventListener('DOMContentLoaded', function() {
                // ページ読み込み時にチェック状態を復元
                const checkboxes = document.querySelectorAll('.search-checkbox');
                checkboxes.forEach(checkbox => {
                    const checkboxId = checkbox.getAttribute('data-id');
                    if (checkboxId) {
                        const isChecked = localStorage.getItem(`checkbox_${checkboxId}`) === 'true';
                        checkbox.checked = isChecked;
                    }

                    // チェックボックスの変更を監視
                    checkbox.addEventListener('change', function() {
                        const checkboxId = this.getAttribute('data-id');
                        if (checkboxId) {
                            localStorage.setItem(`checkbox_${checkboxId}`, this.checked);
                        }
                    });
                });
            });
        }

        // 初期化関数を呼び出し
        initCheckboxes();
'''

# JavaScriptセクションの最後（</script>の前）に挿入
js_insertion_pattern = r'(</script>\s*</body>)'
html_content = re.sub(
    js_insertion_pattern,
    checkbox_js + r'\1',
    html_content,
    count=1
)

# リンクにチェックボックスを追加
# パターン1: eBay + メルカリの組み合わせ
# 既存: <a href="https://www.ebay.com/..." class="search-link">eBay</a>
#       <a href="https://jp.mercari.com/..." class="search-link">メルカリ</a>

# まず、全てのsearch-linkを抽出してカウンタを使って一意のIDを生成
link_counter = 0

def add_checkbox_to_link(match):
    global link_counter
    link = match.group(0)
    link_text = match.group(2)  # eBay または メルカリ

    # プラットフォームを判定
    platform = 'ebay' if 'eBay' in link_text else 'mercari'

    # data-idを生成
    checkbox_id = f"hermes_{platform}_{link_counter}"
    link_counter += 1

    # チェックボックスを追加
    checkbox = f'<input type="checkbox" class="search-checkbox" data-id="{checkbox_id}">'

    return link + '\n                            ' + checkbox

# search-linkのパターンにマッチ
pattern = r'(<a href="[^"]*" target="_blank" class="search-link">)(eBay|メルカリ)(</a>)'
html_content = re.sub(pattern, add_checkbox_to_link, html_content)

# 保存
output_file = '/Users/naokijodan/Desktop/リサーチファイル/HERMES_市場分析_統合版_2026-01-23.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ チェックボックス機能を追加しました: {output_file}")
print(f"📊 ファイルサイズ: {len(html_content):,} 文字")
print(f"🔗 チェックボックス数: {link_counter} 個")
