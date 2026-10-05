# Can a program set a Blogger post's "Search description"? (research, 2026-10-05)

**Bottom line:** No supported programmatic route exists in October 2026. The per-post search description can be set only in the Blogger web editor (Post settings → Search description). The best automated option is the **theme route** (route 5). On a post page with no search description, Blogger's own head tags fall back to a snippet of the post body. If the first lines of each post are written as the description, most of the SEO and social benefit comes without touching the field.

## How this was researched (limits)

- The network policy in this environment blocks `developers.google.com`, `support.google.com`, `*.blogger.com`, `*.blogspot.com` and most theme-developer blogs, both for WebFetch and curl. Evidence therefore comes from:
  1. **Google's official Blogger v3 discovery document**, the machine-readable API schema. I took it from the `google-api-python-client` 2.201.0 wheel on PyPI (`googleapiclient/discovery_cache/documents/blogger.v3.json`, `revision: 20260707`). Primary source, read directly.
  2. **Web-search result snippets** for everything else. These are search-engine summaries of the cited pages, not my own reading of them. Each one is marked *(snippet)* below.
- Nothing was published and the blog was not touched. No credentials were read or used.
- To confirm the theme and feed behaviour empirically, use this repo's manual workflow `.github/workflows/live-check.yml` (Actions → Live page check). It runs outside this network policy and prints the post's `description`/`og:*` tags plus the `summary` of its entry in `feeds/posts/default` and `feeds/posts/summary`.

---

## Route 1: Blogger API v3 (`googleapis.com/blogger/v3`): **No**

**Evidence**

- **Official schema (primary).** The `Post` resource in `blogger.v3.json` (revision 20260707) has exactly these properties: `author, blog, content, customMetaData, etag, id, images, kind, labels, location, published, readerComments, replies, selfLink, status, title, titleLink, trashed, updated, url`. None is a description, summary or search description. `customMetaData` is described only as *"The JSON meta-data for the Post."* (type string). A grep of the whole document for `metaDescription` / `searchDescription` / "search description" finds nothing. The `posts` methods are `delete, get, getByPath, insert, list, patch, publish, revert, search, update`. OAuth scopes are `https://www.googleapis.com/auth/blogger` and `.../blogger.readonly`.
  - Package: https://pypi.org/project/google-api-python-client/ (2.201.0)
  - The same field list appears in the generated client docs:
    - Java: https://developers.google.com/resources/api-libraries/documentation/blogger/v3/java/latest/com/google/api/services/blogger/model/Post.html
    - Go: https://pkg.go.dev/google.golang.org/api/blogger/v3
    - .NET: https://googleapis.dev/dotnet/Google.Apis.Blogger.v3/latest/api/Google.Apis.Blogger.v3.Data.Post.html
    - Java client: https://googleapis.dev/java/google-api-services-blogger/latest/com/google/api/services/blogger/Blogger.html (rev20260707)
  - Official reference page (blocked here, not read): https://developers.google.com/blogger/docs/3.0/reference/posts
- **`customMetaData`:** no Google documentation, issue-tracker entry or answer found that ties it to the search description. Search-engine summaries state that data written to it does not show in the editor's Search description box and is not output as a meta description *(snippet; no primary source behind that claim, so treat it as consistent with the schema rather than as proof)*.
- **GitHub issue googleapis/google-api-python-client#1155, "Blogger API V3 Search Description"** (opened 2021-01-10). A user asks how to set the search description through v3. The issue was labelled question / "Not an issue" and closed with no method given *(snippet)*. https://github.com/googleapis/google-api-python-client/issues/1155
- **The API is otherwise alive.** An August 2026 write-up confirms v3 insert/update/publish works with OAuth refresh tokens and lists no description field *(snippet)*. https://dev.to/just_a_side_project/the-blogger-api-is-still-alive-in-2026-heres-proof-and-working-code-ei8

**Verdict:** No v3 field carries or sets the per-post search description. `customMetaData` is an opaque string with no documented link to it. Writing it is harmless but should not be expected to have any effect. A one-off experiment (patch `customMetaData` on a draft, then look at the editor) would settle it for certain, but nothing found suggests it would work.

## Route 2: Old GData API v2 (Atom, `www.blogger.com/feeds/<blogId>/posts/default`): **Dead for writes**

**Evidence**

- **Blogger Help, "Deprecation notice: Blogger v2.0 GData API scheduled for sunset"** *(snippet)*. The v2.0 GData API was shut down on **2024-09-30**. Its URLs continue to be served only as **feed URLs**. The response is the same as the public `https://<sub>.blogspot.com/feeds/posts/default` feed. Drafts and scheduled posts aren't listed, private blogs return 401, and the notice points users to v3. https://support.google.com/blogger/answer/14877110?hl=en (also listed under https://support.google.com/blogger/announcements/10475244?hl=en)
- Legacy protocol guide (now historical): https://developers.google.com/blogger/docs/2.0/developers_guide_protocol, and the reference guide https://developers.google.com/blogger/docs/2.0/reference
- **Writes.** Because the endpoint is now a read-only public feed, an authenticated POST/PUT with an OAuth 2 bearer token (formerly scope `https://www.blogger.com/feeds/`, header `GData-Version: 2`) has nowhere to go. I could not test it because the host is blocked, but Google's notice leaves no write path.
- **Does `<summary>` map to the search description?** No evidence found that it does. Widget-developer references describe `feed.entry[i].summary.$t` as **a short snippet of the post content**. It appears only when the blog's *Site feed* length is set to *Short* or *Until Jump Break*. None of them say it shows the search description *(snippets)*:
  - https://www.mybloggertricks.com/2016/04/blogger-json-feed-api.html
  - https://www.mybloggertricks.com/2015/10/extract-post-excerpt-via-json.html
  - https://www.danpros.com/post/blogger-json-feed-api
  - https://www.consumingexperience.com/2008/07/blogger-unofficial-feed-faq.html (default vs. summary feeds follow the blog's feed setting)
  - The search for widget-developer reports such as "feed summary shows the search description" turned up none.

**Verdict:** Not usable. The write API was turned down on 2024-09-30. On read, the feeds' `<summary>` is, as far as anyone documents, an auto-excerpt that depends on the feed-length setting, not the search description. `live-check.yml` prints the `summary` of a post's feed entry, which would confirm this on our blog.

## Route 3: Export/import Atom (`feed.atom`, Takeout): **No documented element; import doesn't set it**

**Evidence**

- No `<blogger:metaDescription>` or any other description element is documented anywhere I could find. The newer export (Settings → Back up / Google Takeout → `Takeout/Blogger/Blogs/<blog>/feed.atom`) does use `blogger:` namespace elements. One developer reads `blogger:filename`, for example. No source lists a description element *(snippets)*:
  - https://too-clever-by-half.blogspot.com/2025/06/google-takeout-for-blogger-backup-blog.html
  - https://www.deriasworld.com/2026/08/how-to-back-up-your-blogger-blog-using.html
  - https://ikso.us/posts/migrating-from-blogger/
- Documentation for the old export format says it contains only standard Atom elements, the same as the GData post/comment feeds *(snippet)*: https://developers.google.com/blogger/docs/2.0/reference
- A June 2025 bulk-import guide says Blogger **does not import Search Description, Permalink or Options**, which must be set by hand after import *(snippet)*: https://blogging.realhappinesscenter.com/2025/06/How%20to%20Bulk%20Import%20Posts%20into%20your%20Blogger%20blog%20using%20this%20free%20XML%20template.html

**Verdict:** Not a route. Even if an export happened to contain the value, importing does not reportedly restore it. Bulk import also creates new posts rather than updating existing ones, so it is the wrong tool in any case.

## Route 4: Other routes (Apps Script, editor-internal calls, browser automation)

- **Google Apps Script:** has no Blogger service of its own and would call the same v3 REST API through `UrlFetchApp` or the Advanced Service, so it hits the same limit as route 1. **No.**
- **The web editor's internal endpoints:** the Blogger editor saves posts through private, undocumented calls on `www.blogger.com`. Replaying them needs a logged-in Google session cookie rather than an OAuth API token, and they can change without notice. Google's Terms of Service (https://policies.google.com/terms, paraphrased from memory, not fetched) prohibit accessing services other than through the interfaces and instructions Google provides. Automating them risks the account. **Technically possible, not recommended.** No public, maintained project doing this was found.
- **Browser automation** (Playwright/Selenium driving the editor UI while logged in): this works in principle and is the only way to fill the actual field automatically. Downsides:
  - It needs the account's Google login in a headless browser, which is fragile (2-step verification, "unusual sign-in" challenges).
  - The editor's UI changes break selectors.
  - The same ToS concern about automated access applies, though it is milder than replaying private RPCs.
  - Practical only as a supervised, occasional batch run on someone's own machine, not in CI.
- **Browser extensions:** none found that set Blogger search descriptions.

**Verdict:** Only UI automation can fill the real field. It is fragile and ToS-grey, so it isn't worth it while the theme route covers most of the value.

## Route 5: Theme route (layouts v3): **Yes, and it is the practical answer**

**What the data tags hold** *(snippets; the official tag list is at https://support.google.com/blogger/answer/47270?hl=en, blocked here)*

- **`data:view.description`** is the universal page description. It holds the post's search description when one is set. On a post page **without** one, it holds a **snippet of the post body**, not the blog description. On the home page it is the blog's description (or the blog search description).
  - https://bloggercode.orbiona.com/1978/05/data-view-description.html
- **`data:blog.metaDescription`** holds the blog's search description on the home page and the post's search description on item/static pages. It is **empty** when none is set. Themes therefore wrap it in `<b:if cond='data:blog.metaDescription'>`.
  - https://sneeit.com/blogger-basic-global-layout-data-tags/
  - https://blog.bloggertheme9.com/2026/09/add-meta-description-blogger.html (2026-09)
- **`data:post.metaDescription` / `data:post.snippet`** for `og:description`: per Nitecruzr (2016), these "don't actually exist". `data:blog.metaDescription` is the tag to use.
  - https://blogging.nitecruzr.net/2016/02/using-meta-search-description-in-your.html

**What `<b:include data='blog' name='all-head-content'/>` outputs** *(snippets)*

- **`<meta name="description">`** is output **only when a search description exists** (`data:blog.metaDescription`). A post without one gets **no** meta description tag. Google then picks its own snippet from the page text.
  - https://blog.bloggertheme9.com/2026/09/add-meta-description-blogger.html
  - https://www.mybloggertricks.com/2013/03/Duplicate-Meta-Description-Error.html
- **`og:description`** is always output and uses the page description. That is the search description when set, **otherwise the excerpt from the beginning of the post body**, i.e. `data:view.description`.
  - https://bloggercode.orbiona.com/1981/01/XML-renderer-all-head-content.html
  - https://www.nagahitoyuki.com/2018/08/i-decompose-blogger-data-tags-all-head-content-for-customization-in-the-head-of-my-blogger-blog-template.html (2018, breaks down `all-head-content`)
  - https://fujilogic.blogspot.com/2021/03/optimized-meta-tags.html (2021)

| Post state | `meta name="description"` | `og:description` | `data:view.description` |
|---|---|---|---|
| Search description set | the search description | the search description | the search description |
| No search description | **absent** | snippet from the start of the post body | snippet of the post body |
| Home page, blog search description set | blog search description | blog search description | blog description |

**What the theme can do:**

- Add `<b:if cond='not data:blog.metaDescription and data:view.isPost'><meta name='description' expr:content='data:view.description'/></b:if>` after `all-head-content`. That gives every post a meta description from its own snippet, with no duplicate tag when a real one exists.
- Start every post with a self-contained 140–160 character summary sentence. Both the snippet fallback and Google's own snippet choice then show good text.

Run `live-check.yml` on one post with a search description and one without, to confirm the table above on our theme before changing it.

**Verdict:** Supported, fully automatable through what we publish, and needs no Google login automation. Recommended.

---

## Verdicts at a glance

| Route | Can it set the search description? | Recommendation |
|---|---|---|
| 1. Blogger API v3 (incl. `customMetaData`) | No: no such field in the official schema (rev 20260707) | Don't rely on it |
| 2. GData v2 Atom | No: write API shut down 2024-09-30; `<summary>` is an excerpt | Dead |
| 3. Export/import Atom | No: no documented element; import skips search descriptions | Not a route |
| 4. Apps Script / editor RPC / UI automation | Only UI automation, fragile and ToS-grey | Avoid; manual entry for the few posts that matter |
| 5. Theme (`data:view.description`, `all-head-content`) | Doesn't set the field, but gives posts a good description automatically | **Use this** |
