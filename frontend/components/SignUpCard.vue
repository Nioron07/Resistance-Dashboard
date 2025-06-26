<template>
  <v-card class="mx-auto pa-4" elevation="16" :rounded="0">
    <v-card-title class="text-center text-h5">
      Create an Account
    </v-card-title>
    <v-card-text>
      <!-- Alert for showing success or error messages from the API -->
      <v-alert
        v-if="apiMessage"
        :type="apiError ? 'error' : 'success'"
        variant="tonal"
        density="compact"
        class="mb-4"
        :text="apiMessage"
      ></v-alert>

      <!-- The v-form component with a ref for validation -->
      <v-form ref="form" @submit.prevent="handleSignUp">
        <v-text-field
          v-model="username"
          label="Username"
          :rules="[rules.required]"
          variant="filled"
          required
        ></v-text-field>

        <v-text-field
          v-model="password"
          label="Password"
          :type="showPassword ? 'text' : 'password'"
          :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
          @click:append-inner="showPassword = !showPassword"
          :rules="passwordRules"
          variant="filled"
          required
        ></v-text-field>

        <v-text-field
          v-model="confirmPassword"
          label="Confirm Password"
          type="password"
          :rules="[rules.required, rules.passwordMatch]"
          variant="filled"
          required
        ></v-text-field>

        <v-btn
          type="submit"
          block
          color="primary"
          size="large"
          class="mt-2"
          :rounded="0"
          :loading="isLoading"
          :disabled="isLoading"
        >
          Sign Up
        </v-btn>
      </v-form>
    </v-card-text>
    <v-card-actions class="justify-center">
      <p class="text-center">
        Already have an account? <NuxtLink to="/login" class="text-primary">Login</NuxtLink>
      </p>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';

// Form state
const form = ref<any>(null); // Ref for the v-form instance
const username = ref('');
const password = ref('');
const confirmPassword = ref('');
const showPassword = ref(false);

// UI state
const isLoading = ref(false);
const apiMessage = ref<string | null>(null);
const apiError = ref(false);

const router = useRouter();

// Reusable validation rules
const rules = reactive({
  required: (value: string) => !!value || 'This field is required.',
  passwordMatch: (value: string) => value === password.value || 'Passwords do not match.',
});

// Specific rules for password complexity
const passwordRules = [
  rules.required,
  (v: string) => v.length >= 8 || 'Password must be at least 8 characters.',
  (v: string) => /[A-Z]/.test(v) || 'Must contain an uppercase letter.',
  (v: string) => /[a-z]/.test(v) || 'Must contain a lowercase letter.',
  (v: string) => /[0-9]/.test(v) || 'Must contain a number.',
  (v: string) => /[^A-Za-z0-9]/.test(v) || 'Must contain a special character.',
];

const handleSignUp = async () => {
  // 1. Trigger frontend validation
  const { valid } = await form.value.validate();
  if (!valid) return;

  // 2. Set UI state for API call
  isLoading.value = true;
  apiMessage.value = null;
  apiError.value = false;

  try {
    // 3. Call the backend endpoint
    const response = await fetch('http://localhost:8080/create_account', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      // If the API returns an error, throw it to be caught by the catch block
      throw new Error(data.msg || 'An unknown error occurred.');
    }

    // 4. Handle success
    apiMessage.value = `${data.msg} You will be redirected to login shortly.`;
    // Redirect to login after a short delay
    setTimeout(() => {
      router.push('/login');
    }, 3000);

  } catch (error: any) {
    // 5. Handle errors
    console.error('Sign up failed:', error);
    apiError.value = true;
    apiMessage.value = error.message;
  } finally {
    // 6. Reset loading state
    isLoading.value = false;
  }
};
</script>

<style scoped>
.text-primary {
  color: currentColor;
  text-decoration: none;
}
.text-primary:hover {
  text-decoration: underline;
}
</style>
