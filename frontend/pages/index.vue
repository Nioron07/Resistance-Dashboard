<template>
  <div>
    <!-- The main route guard logic is in the script, but this v-if prevents content flash -->
    <v-container v-if="accountStore.isLoggedIn" fluid>
      <!-- Header -->
      <div class="text-h4 font-weight-bold text-center my-6">
        {{ accountStore.getAccount?.username }}'s Dashboard
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center pa-16">
        <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
        <div class="mt-4">Loading Stats...</div>
      </div>

      <!-- Error State -->
      <v-alert v-else-if="error" type="error" variant="tonal" class="my-4 mx-auto" max-width="800">
        {{ error }}
      </v-alert>

      <!-- Dashboard Content -->
      <div v-else-if="stats">
        <v-row>
          <!-- Overall Performance Panel -->
          <v-col cols="12" md="6">
            <v-card :rounded="0" elevation="8">
              <v-card-item>
                <v-card-title class="d-flex align-center">
                  <v-icon icon="mdi-chart-bar" start color="primary"></v-icon>
                  Overall Performance
                </v-card-title>
              </v-card-item>
              <v-divider></v-divider>
              <v-list-item :title="`${stats.games_won} Games Won`" prepend-icon="mdi-trophy" class="text-success"></v-list-item>
              <v-list-item :title="`${stats.games_lost} Games Lost`" prepend-icon="mdi-emoticon-sad-outline" class="text-error"></v-list-item>
              <v-list-item :title="`${stats.total_games} Total Games Played`" prepend-icon="mdi-gamepad-variant"></v-list-item>
              <v-list-item :title="`${stats.total_score} Total Score`" prepend-icon="mdi-star-circle"></v-list-item>
            </v-card>
          </v-col>

          <!-- Role History Panel -->
          <v-col cols="12" md="6">
            <v-card :rounded="0" elevation="8">
              <v-card-item>
                <v-card-title class="d-flex align-center">
                  <v-icon icon="mdi-account-group" start color="primary"></v-icon>
                  Role History
                </v-card-title>
              </v-card-item>
              <v-divider></v-divider>
              <v-list-item :title="`${stats.times_as_resistance} Times as Resistance`" prepend-icon="mdi-shield-check" class="text-info"></v-list-item>
              <v-list-item :title="`${stats.times_as_spy} Times as Spy`" prepend-icon="mdi-incognito" class="text-error"></v-list-item>
            </v-card>
          </v-col>
        </v-row>
        
        <v-row>
          <!-- Mission & Team Stats -->
          <v-col cols="12" md="6">
            <v-card :rounded="0" elevation="8" class="mt-4">
              <v-card-item>
                <v-card-title class="d-flex align-center">
                  <v-icon icon="mdi-flag-checkered" start color="primary"></v-icon>
                  Mission & Team Stats
                </v-card-title>
              </v-card-item>
              <v-divider></v-divider>
              <v-list-item :title="`${stats.favorable_missions} Favorable Missions`" prepend-icon="mdi-check-circle" class="text-success"></v-list-item>
              <v-list-item :title="`${stats.unfavorable_missions} Unfavorable Missions`" prepend-icon="mdi-close-circle" class="text-error"></v-list-item>
              <v-divider></v-divider>
              <v-list-item :title="`${stats.favorable_teams} Favorable Teams`" prepend-icon="mdi-thumb-up" class="text-success"></v-list-item>
              <v-list-item :title="`${stats.unfavorable_teams} Unfavorable Teams`" prepend-icon="mdi-thumb-down" class="text-error"></v-list-item>
            </v-card>
          </v-col>

          <!-- Commander & Spy Gameplay -->
          <v-col cols="12" md="6">
            <v-card :rounded="0" elevation="8" class="mt-4">
              <v-card-item>
                <v-card-title class="d-flex align-center">
                  <v-icon icon="mdi-crown" start color="primary"></v-icon>
                  Commander & Spy Gameplay
                </v-card-title>
              </v-card-item>
              <v-divider></v-divider>
              <v-list-item :title="`${stats.picked_commander} Times Picked Commander`" prepend-icon="mdi-hand-pointing-up"></v-list-item>
              <v-list-item :title="`${stats.found_as_commander} Times Found as Commander`" prepend-icon="mdi-magnify-scan" class="text-success"></v-list-item>
              <v-divider></v-divider>
              <v-list-item :title="`${stats.players_fooled} Players Fooled`" prepend-icon="mdi-emoticon-cool" class="text-success"></v-list-item>
              <v-list-item :title="`${stats.players_not_fooled} Players Not Fooled`" prepend-icon="mdi-emoticon-neutral" class="text-warning"></v-list-item>
            </v-card>
          </v-col>
        </v-row>
        
      </div>

      <!-- Logout Button (optional, can be in layout) -->
      <div class="text-center my-8">
        <v-btn color="secondary" @click="handleLogout" :rounded="0">
          Logout
        </v-btn>
      </div>

    </v-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAccountStore } from '~/stores/app';

// Set the title for the browser tab
definePageMeta({
  title: 'Dashboard',
});

// Initialize Pinia store
const accountStore = useAccountStore();

// --- STATE FOR THE DASHBOARD ---
const stats = ref<any>(null);
const loading = ref(true);
const error = ref<string | null>(null);

// --- ROUTE GUARD ---
// Redirect to login if not authenticated.
if (!accountStore.isLoggedIn) {
  await navigateTo('/login');
}

// --- DATA FETCHING ---
const fetchStats = async () => {
  const username = accountStore.getAccount?.username;
  if (!username) {
    error.value = "Could not find username to fetch stats.";
    loading.value = false;
    return;
  }

  try {
    const response = await fetch(`http://localhost:8080/getAccountInfo?username=${username}`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.msg || 'Failed to fetch account statistics.');
    }
    stats.value = data;
  } catch (e: any) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
};

// --- LOGOUT LOGIC ---
const handleLogout = async () => {
  accountStore.clearAccount();
  await navigateTo('/login');
};

// --- LIFECYCLE HOOK ---
// Fetch stats when the component is mounted (after login).
onMounted(() => {
  // Only fetch if the user is actually logged in.
  if (accountStore.isLoggedIn) {
    fetchStats();
  } else {
    // This is a fallback in case the guard fails for any reason
    loading.value = false;
    error.value = "You are not logged in.";
  }
});
</script>

<style scoped>
/* You can add component-specific styles here */
.text-success {
  color: #43A047 !important;
}
.text-error {
  color: #D32F2F !important;
}
.text-warning {
  color: #F57C00 !important;
}
.text-info {
  color: #1976D2 !important;
}
</style>
