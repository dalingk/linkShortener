%if defined('error'):
<p class="center">{{error}}</p>
%elif defined('stats'):
<section>
    <div class="links">
        <a href="/l/{{stats['tiny']}}" rel="nofollow">{{stats['name']}}</a>
    </div>
    <div>
        <dl class="stats">
            <div>
                <dt>Name</dt>
                <dd>{{stats['name']}}</dd>
            </div>
            <div>
                <dt>URL</dt>
                <dd>{{stats['url']}}</dd>
            </div>
            <div>
                <dt>Tiny URL</dt>
                <dd><a href="/l/{{stats['tiny']}}">{{stats['tiny']}}</a></dd>
            </div>
            %if "createdBy" in stats:
            <div>
                <dt>Created By</dt>
                <dd>{{stats['createdBy']}}</dd>
            </div>
            %end
            %if 'private' in stats:
            <div title="Note: Private links are can still be shared, but do not show up in results">
                <dt>Private</dt>
                <dd>{{"Yes" if stats['private'] == 1 else "No"}}</dd>
            </div>
            %end
            %if "createdTime" in stats:
            <div>
                <dt>Created</dt>
                <dd>{{stats['createdTime']}} ago</dd>
            </div>
            %end
            %if "createdIP" in stats:
            <div>
                <dt>Created IP</dt>
                <dd>{{stats['createdIP']}}</dd>
            </div>
            %end
            %if 'numViews' in stats and stats['numViews'] > 0:
            <div><dt>Views</dt><dd>{{stats['numViews']}}</dd></div>
            <div><dt>Last Viewed</dt><dd>{{stats['lastView']}} ago</dd></div>
            <div><dt>IP of last viewer</dt><dd>{{stats['lastViewIP']}}</dd></div>
            %end
        </dl>
    </div>
</section>
%else:
<label class="stats"><input type="checkbox" id="stats"> Go to links</label>
<section class="links">
    %for x in links:
    <a href="/stats/{{x[2]}}" title="{{x[1]}}" {{!"class=\"private\"" if len(x) > 3 and x[3] == 1 else ""}}>{{x[0]}}</a>
    %end
</section>
%end
% rebase('layout.tpl', title=title)
