<template>
  <v-card class="mx-auto pa-4" elevation="16" max-width="448" :rounded="0">
    <div v-if="accountStore.isLoggedIn">
      <v-card-title>Welcome, {{ accountStore.getAccount?.username }}</v-card-title>
      <v-card-text>You are logged in!</v-card-text>
      <v-card-actions>
        <v-btn @click="handleLogout" color="secondary" block :rounded="0">Logout</v-btn>
      </v-card-actions>
    </div>

    <div v-else>
      <v-card-title class="text-center text-h5">
        Member Login
      </v-card-title>
      <v-card-text>
        <!-- Display API errors here -->
        <v-alert
          v-if="errorMessage"
          type="error"
          variant="tonal"
          density="compact"
          class="mb-4"
          :text="errorMessage"
        ></v-alert>

        <v-form @submit.prevent="handleLogin">
          <v-text-field
            v-model="username"
            label="Username"
            variant="filled"
            required
            @focus="errorMessage = null"
          ></v-text-field>
          <v-text-field
            v-model="password"
            label="Password"
            type="password"
            variant="filled"
            required
            @focus="errorMessage = null"
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
            Login
          </v-btn>
        </v-form>
      </v-card-text>
      <v-card-actions class="justify-center">
        <p class="text-center">
          Don't have an account? <NuxtLink to="/signup" class="text-primary">Sign Up</NuxtLink>
        </p>
      </v-card-actions>
    </div>
  </v-card>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAccountStore } from '~/stores/app';

const accountStore = useAccountStore();
const username = ref(null);
const password = ref(null);

// Refs for UI state
const isLoading = ref(false);
const errorMessage = ref<string | null>(null);

const handleLogin = async () => {
  isLoading.value = true;
  errorMessage.value = null;

  try {
    const response = await fetch('http://127.0.0.1:8080/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      // If response is not 2xx, throw an error with the message from the backend
      throw new Error(data.msg || 'An error occurred.');
    }

    // On success, update the store with the returned account info
    accountStore.setAccount(data);

    // Redirect to the homepage
    await navigateTo('/');

  } catch (error: any) {
    console.error('Login failed:', error);
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
};

const handleLogout = async () => {
  accountStore.clearAccount();
  await navigateTo('/login');
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
