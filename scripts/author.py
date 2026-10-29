"""Who writes Verdict Picks (daily/profhlab-link-plan-2026-10-29.md, section 3, step 1): one real, named author across the blog.

Prof. H is the pen name of the site's owner, a professor of AI and robotics, a former Samsung researcher and the author of
textbooks on AI and automation, who also runs Prof H Lab (profhlab.com). The byline names the field honestly: the expertise
is AI and robotics; for bidets, pillows or dog beds Prof. H is the editor and the guide rests on cited tests and owner
reports (the About page says so). assemble_post.py swaps the old "Verdict Picks editors" byline for this one whenever a
post is rebuilt, so posts change one at a time on improve days, never in one mass republish.
"""
ABOUT = "/p/about-verdict-picks.html#prof-h"
LAB = "https://profhlab.com/about/"
OLD_BYLINE = 'By the <a href="/p/about-verdict-picks.html">Verdict Picks editors</a>'
BYLINE = f'By <a href="{ABOUT}">Prof. H</a>, professor of AI and robotics (<a href="{LAB}">Prof H Lab</a>)'
PERSON = {"@type": "Person", "name": "Prof. H", "jobTitle": "Professor of AI and robotics",
          "url": "https://acts39.blogspot.com" + ABOUT, "sameAs": [LAB]}
