with open("index.html", "r") as f:
    html = f.read()

import re
old_script = """    // Fix broken eventrix images aggressively
    let images = document.querySelectorAll('img');
    for (let img of images) {
        if (img.src && (img.src.includes('usersFiles') || img.src.includes('invitePhoto') || img.src.includes('%2FusersFiles'))) {
            if (!img.dataset.fixed) {
                img.dataset.fixed = '1';
                // Remove Next.js srcset which overrides src
                img.removeAttribute('srcset');
                img.removeAttribute('sizes');
                
                if (img.src.includes('inviteMainPhoto') || img.src.includes('%2FinviteMainPhoto')) {
                    img.src = '/4.png';
                } else {
                    img.src = '/3.png';
                }
            }
        }
    }
    
    // Fix broken background images
    let allElements = document.querySelectorAll('*');
    for (let el of allElements) {
        let bg = el.style.backgroundImage;
        if (bg && (bg.includes('usersFiles') || bg.includes('invitePhoto') || bg.includes('%2FusersFiles'))) {
            if (!el.dataset.fixedBg) {
                el.dataset.fixedBg = '1';
                if (bg.includes('inviteMainPhoto') || bg.includes('%2FinviteMainPhoto')) {
                    el.style.backgroundImage = 'url(/4.png)';
                } else {
                    el.style.backgroundImage = 'url(/3.png)';
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
                    img.src = '/photo1.jpg';
                } else if (img.src.includes('invitePhoto2x') || img.src.includes('%2FinvitePhoto2x')) {
                    img.src = '/photo3.jpg';
                } else {
                    img.src = '/photo2.jpg';
                }
            }
        }
    }
    
    // Fix broken background images
    let allElements = document.querySelectorAll('*');
    for (let el of allElements) {
        let bg = el.style.backgroundImage;
        if (bg && (bg.includes('usersFiles') || bg.includes('invitePhoto') || bg.includes('%2FusersFiles'))) {
            if (!el.dataset.fixedBg) {
                el.dataset.fixedBg = '1';
                if (bg.includes('inviteMainPhoto') || bg.includes('%2FinviteMainPhoto')) {
                    el.style.backgroundImage = 'url(/photo1.jpg)';
                } else if (bg.includes('invitePhoto2x') || bg.includes('%2FinvitePhoto2x')) {
                    el.style.backgroundImage = 'url(/photo3.jpg)';
                } else {
                    el.style.backgroundImage = 'url(/photo2.jpg)';
                }
            }
        }
    }"""

html = html.replace(old_script, new_script)

with open("index.html", "w") as f:
    f.write(html)
