with open("index.html", "r") as f:
    html = f.read()

import re
old_script = """    // Fix broken eventrix images
    let images = document.querySelectorAll('img');
    for (let img of images) {
        if (img.src && img.src.includes('eventrix.pro') && img.src.includes('usersFiles')) {
            if (!img.dataset.fixed) {
                img.dataset.fixed = '1';
                if (img.src.includes('inviteMainPhoto')) {
                    img.src = '/og-image.jpg'; // Main photo fallback
                    img.srcset = '';
                } else {
                    img.src = '/3.png'; // Story photo fallback
                    img.srcset = '';
                }
            }
        }
    }"""

new_script = """    // Fix broken eventrix images aggressively
    let images = document.querySelectorAll('img');
    for (let img of images) {
        if (img.src && (img.src.includes('usersFiles') || img.src.includes('invitePhoto') || img.src.includes('%2FusersFiles'))) {
            if (!img.dataset.fixed) {
                img.dataset.fixed = '1';
                // Remove Next.js srcset which overrides src
                img.removeAttribute('srcset');
                img.removeAttribute('sizes');
                
                if (img.src.includes('inviteMainPhoto') || img.src.includes('%2FinviteMainPhoto')) {
                    img.src = '/og-image.jpg';
                } else {
                    img.src = '/3.png';
                }
            }
        }
    }"""

html = html.replace(old_script, new_script)

with open("index.html", "w") as f:
    f.write(html)
