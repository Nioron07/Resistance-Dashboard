import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

/**
 * Interface for the Account object.
 * Using an interface provides strong type safety for your state.
 */
export interface Account {
  id: string;
  username: string;
}

/**
 * Defines the Pinia store for account management.
 * The first argument 'account' is the unique ID of the store.
 */
export const useAccountStore = defineStore('app', () => {
  // --- STATE ---
  // The 'ref' function creates a reactive variable to hold the state.
  // We initialize it as null because the user is not logged in initially.
  const account = ref<Account | null>(null);

  // --- GETTERS ---
  // Getters are implemented as computed properties. They are cached and
  // only re-evaluate when their dependencies change.

  /**
   * Getter to safely access the account information.
   */
  const getAccount = computed(() => account.value);

  /**
   * A boolean getter to quickly check if a user is logged in.
   */
  const isLoggedIn = computed(() => !!account.value?.id);

  // --- ACTIONS ---
  // Actions are functions that can be called from components to
  // modify the state.

  /**
   * Sets the account state. This acts as our "setter".
   * This would be called after a successful login API call.
   * @param {Account} newAccount - The user account object.
   */
  function setAccount(newAccount: Account) {
    account.value = newAccount;
  }

  /**
   * Clears the account state.
   * This would be called on logout.
   */
  function clearAccount() {
    account.value = null;
  }

  // --- RETURN ---
  // The store must return all the state, getters, and actions
  // that you want to expose to your components.
  return {
    account, // You can expose the raw state if needed
    getAccount,
    isLoggedIn,
    setAccount,
    clearAccount,
  };
},
{
  persist: true,
});
