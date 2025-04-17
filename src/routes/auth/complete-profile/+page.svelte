<script lang="ts">
    import { onMount, getContext } from 'svelte';
    import { goto } from '$app/navigation';
    import { toast } from 'svelte-sonner';
    import { user } from '$lib/stores';
    
    const i18n = getContext('i18n');
    
    let gender = '';
    let country = '';
    let birthdate = '';
    let preferredLanguage = '';
    let interactionType = 'chat'; // Default a chat
    let interests = [];
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
    
    // Languages list
    const languages = [
        { value: 'italian', label: 'Italiano' },
        { value: 'english', label: 'English' },
        { value: 'spanish', label: 'Español' },
        { value: 'french', label: 'Français' },
        { value: 'german', label: 'Deutsch' }
    ];
    
    // Interaction types
    const interactionTypes = [
        { value: 'chat', label: $i18n.t('Chat') },
        { value: 'audio', label: $i18n.t('Audio') }
    ];
    
    // Interests list
    const interestOptions = [
        { value: 'technology', label: $i18n.t('Technology') },
        { value: 'science', label: $i18n.t('Science') },
        { value: 'arts', label: $i18n.t('Arts') },
        { value: 'sports', label: $i18n.t('Sports') },
        { value: 'travel', label: $i18n.t('Travel') },
        { value: 'cooking', label: $i18n.t('Cooking') },
        { value: 'reading', label: $i18n.t('Reading') },
        { value: 'music', label: $i18n.t('Music') },
        { value: 'movies', label: $i18n.t('Movies') },
        { value: 'gaming', label: $i18n.t('Gaming') },
        { value: 'education', label: $i18n.t('Education') },
        { value: 'business', label: $i18n.t('Business') },
        { value: 'health', label: $i18n.t('Health') },
        { value: 'fashion', label: $i18n.t('Fashion') },
        { value: 'photography', label: $i18n.t('Photography') }
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
    
    const toggleInterest = (value) => {
        if (interests.includes(value)) {
            interests = interests.filter(item => item !== value);
        } else {
            interests = [...interests, value];
        }
    };
    
    const submitProfile = async () => {
        if (!gender || !country || !birthdate || !preferredLanguage || !interactionType || interests.length === 0) {
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
                body: JSON.stringify({ 
                    gender, 
                    country, 
                    birthdate,
                    preferred_language: preferredLanguage,
                    interaction_type: interactionType,
                    interests
                })
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
    <div class="w-full max-w-lg p-6 rounded-xl shadow-lg bg-card">
        <h1 class="text-2xl font-semibold mb-4 text-center">{$i18n.t('Complete Your Profile')}</h1>
        
        <p class="mb-6 text-center">
            {$i18n.t('Please provide some additional information to complete your profile.')}
        </p>
        
        <div class="space-y-4">
            <!-- Gender -->
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
            
            <!-- Country -->
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
            
            <!-- Birthdate -->
            <div class="mb-4">
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
            
            <!-- Preferred Language -->
            <div class="mb-4">
                <label for="language" class="block mb-2 font-medium text-card-foreground">
                    {$i18n.t('Preferred Language')}
                </label>
                <select
                    id="language"
                    bind:value={preferredLanguage}
                    class="w-full p-2 rounded-md border bg-input focus:ring-2 focus:ring-primary"
                >
                    <option value="" disabled selected>{$i18n.t('Select your preferred language')}</option>
                    {#each languages as lang}
                        <option value={lang.value}>{lang.label}</option>
                    {/each}
                </select>
            </div>
            
            <!-- Interaction Type -->
            <div class="mb-4">
                <label class="block mb-2 font-medium text-card-foreground">
                    {$i18n.t('Preferred Interaction Type')}
                </label>
                <div class="flex gap-4">
                    {#each interactionTypes as type}
                        <label class="flex items-center space-x-2 cursor-pointer">
                            <input 
                                type="radio" 
                                name="interactionType" 
                                value={type.value} 
                                bind:group={interactionType}
                                class="w-4 h-4 text-primary accent-primary"
                            />
                            <span>{type.label}</span>
                        </label>
                    {/each}
                </div>
            </div>
            
            <!-- Interests -->
            <div class="mb-6">
                <label class="block mb-2 font-medium text-card-foreground">
                    {$i18n.t('Interests')} <span class="text-xs text-gray-500">({$i18n.t('Select at least one')})</span>
                </label>
                <div class="grid grid-cols-2 sm:grid-cols-3 gap-2">
                    {#each interestOptions as interest}
                        <label class="flex items-center space-x-2 cursor-pointer p-2 rounded-md hover:bg-gray-50 dark:hover:bg-gray-800">
                            <input 
                                type="checkbox" 
                                value={interest.value} 
                                checked={interests.includes(interest.value)}
                                on:change={() => toggleInterest(interest.value)}
                                class="w-4 h-4 text-primary accent-primary"
                            />
                            <span>{interest.label}</span>
                        </label>
                    {/each}
                </div>
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