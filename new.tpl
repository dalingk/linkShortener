<form method="post" class="add">
    <label><span>URL:</span><input type="text" placeholder="https://" name="url" autofocus required></label>
    <label><span>Link Name:</span><input type="text" placeholder="Link Name" name="name"></label>
    %if custom:
    <label><span>Custom:</span><input type="text" placeholder="Short URL" name="custom"></label>
    %end
    <label><input type="submit"></label>
</form>
% rebase('layout.tpl', title=title)
