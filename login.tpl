<form method="post" class="add">
%if defined('error'):
<p class="error">{{error}}</p>
%end
    <label><span>Email:</span><input type="email" placeholder="test@example.com" name="email" autofocus required></label>
    <label><span>Password (or login token):</span><input type="password" placeholder="Password" name="password" required></label>
    <label><input type="submit"></label>
</form>
<p class="center"><a href="/register">Register</a> if you don't have an account.</p>
% rebase('layout.tpl', title=title)
