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
                <dd><a href="https://dalingk.co/l/{{stats['tiny']}}">https://dalingk.co/l/{{stats['tiny']}}</a></dd>
            </div>
            %if "createdBy" in stats:
            <div>
                <dt>Created By</dt>
                <dd>{{stats['createdBy']}}</dd>
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
        </dl>
    </div>
    %if 'numViews' in stats and stats['numViews'] > 0:
    <div>
        <dl class="stats">
            <div><dt>Views</dt><dd>{{stats['numViews']}}</dd></div>
            <div><dt>Last Viewed</dt><dd>{{stats['lastView']}} ago</dd></div>
            <div><dt>IP of last viewer</dt><dd>{{stats['lastViewIP']}}</dd></div>
        </dl>
    </div>
</section>
%end
%else:
<label class="stats"><input type="checkbox" id="stats" checked="checked"> Show stats</label>
<section class="links">
    %for x in links:
    <a href="/l/{{x[2]}}" title="{{x[1]}}">{{x[0]}}</a>
    %end
</section>
%end
% rebase('layout.tpl', title=title)
