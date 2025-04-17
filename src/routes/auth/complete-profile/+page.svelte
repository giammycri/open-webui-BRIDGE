<script lang="ts">
    import { onMount, getContext } from 'svelte';
    import { goto } from '$app/navigation';
    import { toast } from 'svelte-sonner';
    import { user } from '$lib/stores';
    
    const i18n = getContext('i18n');
    
    let gender = '';
    let country = '';
    let birthdate = '';
    let isLoading = false;
    
    // European countries list
    const europeanCountries = [
        'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus',
        'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France',
        'Germany', 'Greece', 'Hungary', 'Ireland', 'Italy',
        'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands',
        'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia',
        'Spain', 'Sweden'
    ];
    
    onMount(() => {
        // Check if user is already logged in and profile is completed
        const currentUser = $user;
        if (!currentUser || !currentUser.id) {
            // Redirect to login if not logged in
            toast.error($i18n.t('Please log in first'));
            goto('/auth');
        } else if (currentUser.is_profile_completed) {
            // Redirect to home if profile is already completed
            goto('/');
        }
    });
    
    const submitProfile = async () => {
        if (!gender || !country || !birthdate) {
            toast.error($i18n.t('Please fill in all fields'));
            return;
        }
        
        isLoading = true;
        
        try {
            const response = await fetch('/api/v1/auths/complete-profile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ gender, country, birthdate })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to complete profile');
            }
            
            const data = await response.json();
            
            // Update user store with new profile data
            user.update(u => ({...u, ...data}));
            
            toast.success($i18n.t('Profile completed successfully'));
            goto('/');
        } catch (error) {
            toast.error(error.message || $i18n.t('Failed to complete profile'));
        } finally {
            isLoading = false;
        }
    };
</script>

<div class="flex min-h-screen flex-col items-center justify-center">
    <div class="w-full max-w-md p-6 rounded-xl shadow-lg bg-card">
        <h1 class="text-2xl font-semibold mb-6 text-center">{$i18n.t('Complete Your Profile')}</h1>
        
        <p class="mb-6 text-center">
            {$i18n.t('Please provide some additional information to complete your profile.')}
        </p>
        
        <div class="space-y-4">
            <div class="mb-4">
                <label for="gender" class="block mb-2 font-medium text-card-foreground">
                    {$i18n.t('Gender')}
                </label>
                <select
                    id="gender"
                    bind:value={gender}
                    class="w-full p-2 rounded-md border bg-input focus:ring-2 focus:ring-primary"
                >
                    <option value="" disabled selected>{$i18n.t('Select your gender')}</option>
                    <option value="male">{$i18n.t('Male')}</option>
                    <option value="female">{$i18n.t('Female')}</option>
                    <option value="other">{$i18n.t('Other')}</option>
                    <option value="prefer_not_to_say">{$i18n.t('Prefer not to say')}</option>
                </select>
            </div>
            
            <div class="mb-4">
                <label for="country" class="block mb-2 font-medium text-card-foreground">
                    {$i18n.t('Country')}
                </label>
                <select
                    id="country"
                    bind:value={country}
                    class="w-full p-2 rounded-md border bg-input focus:ring-2 focus:ring-primary"
                >
                    <option value="" disabled selected>{$i18n.t('Select your country')}</option>
                    {#each europeanCountries as euroCountry}
                        <option value={euroCountry}>{euroCountry}</option>
                    {/each}
                </select>
            </div>
            
            <div class="mb-6">
                <label for="birthdate" class="block mb-2 font-medium text-card-foreground">
                    {$i18n.t('Date of Birth')}
                </label>
                <input
                    type="date"
                    id="birthdate"
                    bind:value={birthdate}
                    class="w-full p-2 rounded-md border bg-input focus:ring-2 focus:ring-primary"
                />
            </div>
            
            <button
                on:click={submitProfile}
                disabled={isLoading}
                class="w-full p-2 rounded-md bg-primary text-primary-foreground font-medium hover:opacity-90 transition-opacity disabled:opacity-70"
            >
                {isLoading ? $i18n.t('Submitting...') : $i18n.t('Complete Profile')}
            </button>
        </div>
    </div>
</div>