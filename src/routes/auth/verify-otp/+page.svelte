<script lang="ts">
    import { onMount, getContext } from 'svelte';
    import { goto } from '$app/navigation';
    import { toast } from 'svelte-sonner';
    import { user, config } from '$lib/stores';
    import { getBackendConfig } from '$lib/apis';
    
    const i18n = getContext('i18n');
    
    let email = '';
    let otp = '';
    let isLoading = false;
    
    onMount(() => {
        // Get email from query params or localStorage
        const urlParams = new URLSearchParams(window.location.search);
        email = urlParams.get('email') || localStorage.getItem('pendingEmail') || '';
        
        if (!email) {
            toast.error($i18n.t('Email not found. Please try signing up again.'));
            goto('/auth');
        }
    });
    
    const verifyOtp = async () => {
        if (!otp) {
            toast.error($i18n.t('Please enter verification code.'));
            return;
        }
        
        isLoading = true;
        
        try {
            const response = await fetch('/api/v1/auths/verify-otp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, otp })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.detail || 'Verification failed');
            }
            
            // Successfully verified
            if (data.token) {
                localStorage.token = data.token;
                await user.set(data);
                await config.set(await getBackendConfig());
                toast.success($i18n.t('Account verified successfully.'));
                
                // Controlla se il profilo è completo
                if (!data.is_profile_completed) {
                    goto('/auth/complete-profile');
                } else {
                    goto('/');
                }
            }
        } catch (error) {
            toast.error(error.message || $i18n.t('Verification failed. Please try again.'));
        } finally {
            isLoading = false;
        }
    };
    
    const resendOtp = async () => {
        isLoading = true;
        
        try {
            const response = await fetch('/api/v1/auths/resend-otp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email })
            });
            
            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.detail || 'Failed to resend verification code');
            }
            
            toast.success($i18n.t('Verification code sent. Please check your email.'));
        } catch (error) {
            toast.error(error.message || $i18n.t('Failed to resend verification code.'));
        } finally {
            isLoading = false;
        }
    };
</script>

<div class="flex min-h-screen flex-col items-center justify-center">
    <div class="w-full max-w-md p-6 rounded-xl shadow-lg bg-card">
        <h1 class="text-2xl font-semibold mb-6 text-center">{$i18n.t('Verify your email')}</h1>
        
        <p class="mb-6 text-center">
            {$i18n.t('We sent a verification code to')} <strong>{email}</strong>
            {$i18n.t('Please enter it below.')}
        </p>
        
        <div class="mb-6">
            <label for="otp" class="block mb-2 font-medium text-card-foreground">
                {$i18n.t('Verification Code')}
            </label>
            <input
                type="text"
                id="otp"
                bind:value={otp}
                class="w-full p-2 rounded-md border bg-input focus:ring-2 focus:ring-primary"
                placeholder="123456"
                maxlength="6"
            />
        </div>
        
        <button
            on:click={verifyOtp}
            disabled={isLoading}
            class="w-full p-2 rounded-md bg-primary text-primary-foreground font-medium hover:opacity-90 transition-opacity disabled:opacity-70"
        >
            {isLoading ? $i18n.t('Verifying...') : $i18n.t('Verify')}
        </button>
        
        <div class="mt-4 text-center">
            <button
                on:click={resendOtp}
                disabled={isLoading}
                class="text-primary hover:underline"
            >
                {$i18n.t('Resend verification code')}
            </button>
        </div>
        
        <div class="mt-6 text-center">
            <button
                on:click={() => goto('/auth')}
                class="text-muted-foreground hover:underline"
            >
                {$i18n.t('Back to login')}
            </button>
        </div>
    </div>
</div>