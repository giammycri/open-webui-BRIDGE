<script lang="ts">
	import { toast } from 'svelte-sonner';
	import { onMount, getContext, tick } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	import { WEBUI_NAME } from '$lib/stores';
	import { completeUserProfile } from '$lib/apis/auths';

	const i18n = getContext('i18n');

	// Form data
	let gender = '';
	let country = '';
	let birthdate = '';
	let preferredLanguage = '';
	let interactionType = '';
	let interests = [];

	// Gender options
	const genderOptions = [
		{ value: 'male', label: 'Male' },
		{ value: 'female', label: 'Female' },
		{ value: 'other', label: 'Other' },
		{ value: 'prefer_not_to_say', label: 'Prefer not to say' }
	];

	// Country options (shortened for example)
	const countryOptions = [
		{ value: 'italy', label: 'Italy' },
		{ value: 'united_states', label: 'United States' },
		{ value: 'united_kingdom', label: 'United Kingdom' },
		{ value: 'germany', label: 'Germany' },
		{ value: 'france', label: 'France' },
		{ value: 'spain', label: 'Spain' },
		// Add more countries as needed
	];

	// Language options
	const languageOptions = [
		{ value: 'english', label: 'English' },
		{ value: 'italian', label: 'Italian' },
		{ value: 'spanish', label: 'Spanish' },
		{ value: 'french', label: 'French' },
		{ value: 'german', label: 'German' },
		// Add more languages as needed
	];

	// Interaction type options
	const interactionTypeOptions = [
		{ value: 'casual', label: 'Casual' },
		{ value: 'professional', label: 'Professional' },
		{ value: 'educational', label: 'Educational' }
	];

	// Interest categories
	const interestCategories = [
		'Technology',
		'Science',
		'Arts',
		'Sports',
		'Travel',
		'Music',
		'Books',
		'Movies',
		'Cooking',
		'Health'
	];

	// Handle checkbox changes
	function handleInterestChange(interest, isChecked) {
		if (isChecked) {
			interests = [...interests, interest];
		} else {
			interests = interests.filter(i => i !== interest);
		}
	}

	// Submit the form
	async function submitProfile() {
		try {
			await completeUserProfile({
				gender,
				country,
				birthdate,
				preferred_language: preferredLanguage,
				interaction_type: interactionType,
				interests
			});
			
			toast.success($i18n.t('Profile completed successfully!'));
			goto('/');
		} catch (error) {
			toast.error($i18n.t('Failed to complete profile'));
			console.error(error);
		}
	}
</script>

<svelte:head>
	<title>{$i18n.t('Complete Your Profile')} - {$WEBUI_NAME}</title>
</svelte:head>

<div class="fixed bg-transparent min-h-screen w-full flex justify-center font-primary z-50 text-black dark:text-white">
	<div class="w-full max-w-4xl px-6 py-8 flex flex-col">
		<h1 class="text-2xl font-medium text-center mb-6">{$i18n.t('Complete Your Profile')}</h1>
		
		<form on:submit|preventDefault={submitProfile} class="bg-white dark:bg-gray-800 shadow-md rounded-lg p-6">
			<div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4">
				<!-- Left column -->
				<div class="space-y-4">
					<!-- Gender -->
					<div>
						<label class="block text-sm font-medium mb-1">{$i18n.t('Gender')}</label>
						<select
							bind:value={gender}
							class="w-full bg-transparent border border-gray-300 dark:border-gray-600 rounded p-2 text-sm"
						>
							<option value="">{$i18n.t('Select gender')}</option>
							{#each genderOptions as option}
								<option value={option.value}>{$i18n.t(option.label)}</option>
							{/each}
						</select>
					</div>

					<!-- Country -->
					<div>
						<label class="block text-sm font-medium mb-1">{$i18n.t('Country')}</label>
						<select
							bind:value={country}
							class="w-full bg-transparent border border-gray-300 dark:border-gray-600 rounded p-2 text-sm"
						>
							<option value="">{$i18n.t('Select country')}</option>
							{#each countryOptions as option}
								<option value={option.value}>{$i18n.t(option.label)}</option>
							{/each}
						</select>
					</div>

					<!-- Birthdate -->
					<div>
						<label class="block text-sm font-medium mb-1">{$i18n.t('Birthdate')}</label>
						<input
							type="date"
							bind:value={birthdate}
							class="w-full bg-transparent border border-gray-300 dark:border-gray-600 rounded p-2 text-sm"
						/>
					</div>
				</div>
				
				<!-- Right column -->
				<div class="space-y-4">
					<!-- Preferred Language -->
					<div>
						<label class="block text-sm font-medium mb-1">{$i18n.t('Preferred Language')}</label>
						<select
							bind:value={preferredLanguage}
							class="w-full bg-transparent border border-gray-300 dark:border-gray-600 rounded p-2 text-sm"
						>
							<option value="">{$i18n.t('Select language')}</option>
							{#each languageOptions as option}
								<option value={option.value}>{$i18n.t(option.label)}</option>
							{/each}
						</select>
					</div>

					<!-- Interaction Type -->
					<div>
						<label class="block text-sm font-medium mb-1">{$i18n.t('Interaction Type')}</label>
						<select
							bind:value={interactionType}
							class="w-full bg-transparent border border-gray-300 dark:border-gray-600 rounded p-2 text-sm"
						>
							<option value="">{$i18n.t('Select interaction type')}</option>
							{#each interactionTypeOptions as option}
								<option value={option.value}>{$i18n.t(option.label)}</option>
							{/each}
						</select>
					</div>
				</div>
			</div>

			<!-- Interests (uses full width) -->
			<div class="mt-4">
				<label class="block text-sm font-medium mb-2">{$i18n.t('Interests')}</label>
				<div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2">
					{#each interestCategories as interest}
						<div class="flex items-center">
							<input
								type="checkbox"
								id={interest}
								class="mr-2"
								on:change={(e) => handleInterestChange(interest, e.target.checked)}
							/>
							<label for={interest} class="text-sm">{$i18n.t(interest)}</label>
						</div>
					{/each}
				</div>
			</div>
			
			<!-- Submit button (centered) -->
			<div class="mt-6 text-center">
				<button
					type="submit"
					class="bg-gray-700/5 hover:bg-gray-700/10 dark:bg-gray-100/5 dark:hover:bg-gray-100/10 dark:text-gray-300 dark:hover:text-white transition w-full max-w-xs rounded-full font-medium text-sm py-2.5"
				>
					{$i18n.t('Complete Profile')}
				</button>
			</div>
		</form>
	</div>
</div>