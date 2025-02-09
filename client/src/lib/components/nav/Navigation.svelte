
<script>
    import { page } from '$app/state';
    import { url } from '$utils/url';

    import NavLink from '$components/nav/NavLink.svelte';

</script>
<div class="flex flex-col justify-between h-full w-32">
    <nav class="list-nav">
        <ul class="">
            <li><NavLink title="Home" href="/"/></li>
            <li><NavLink title="Games" href="/games"/></li>
            <li><NavLink title="Projects" href="/projects"/></li>
            <li><NavLink title="About" href="/about"/></li>
        </ul>

        <hr class="my-4">

        <ul class="">
            <li><NavLink title="Recipe" href="/recipe"/></li>
        </ul>
    </nav>

    <nav class="list-nav">
        <ul>
        {#if page.data.user}
            <li><NavLink title="My Profile" href="/profile"></NavLink></li>
            
            <li>
                <form method="POST" action="{url("logout")}">
                    <button class="w-full text-left px-2">Logout</button>
                </form>
            </li>
        {:else}
            <li><NavLink title="Login" href="{url("login")}?redirectTo={page.url.pathname}"/></li>
            <li><NavLink title="Signup" href="{url("signup")}?redirectTo={page.url.pathname}"/></li>
        {/if}
        </ul>
    </nav>
</div>