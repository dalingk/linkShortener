%if defined('email') and not defined('error'):
<div class="center">
    <p>Registration for <strong>{{email}}</strong> complete.</p>
    <p>Go ahead and <a href="/login">login</a>.</p>
    <p>Back to <a href="/">home</a>?</p>
</div>
%else:
%if defined('error'):
<p class="error">{{error}}</p>
%end
<form method="post" class="add">
    <label><span>Email:</span><input type="email" placeholder="test@example.com" name="email" value="{{email if defined("email") else ""}}" autofocus required></label>
    <label><span>Password:</span><input type="password" placeholder="Password" name="password" required></label>
    <label><span>Confirm password:</span><input type="password" name="confirm" required></label>
    <label><input type="submit"></label>
</form>
<p class="center"><a href="/login">Login</a> if you already have an account.</p>
%end
% rebase('layout.tpl', title=title)
