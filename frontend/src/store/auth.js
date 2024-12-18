import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', {
  state: () => {
    const storedState = localStorage.getItem('authState')
    return storedState ? JSON.parse(storedState) : {
      user: null,
      isAuthenticated: false
    }
  },
  actions: {
    async setCsrfToken() {
      await fetch('http://localhost:8000/api/set-csrf-token', {
        method: 'GET',
        credentials: 'include'
      })
    },

    async login(username, password, router=null) {
      console.log(username, password)
      const response = await fetch('http://localhost:8000/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
      },
      body: JSON.stringify({ username, password }),
      credentials: 'include'
      })
      const data = await response.json()

      if (data.success) {
      this.isAuthenticated = true
      this.saveState()
      console.log(router)
      if (router){
        await router.push({name: "home"})
      }
      } else {
      this.user = null
      this.isAuthenticated = false
      this.saveState()
      }
    },

    async logout(router=null) {
      try {
        const response = await fetch('http://localhost:8000/api/logout', {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCSRFToken()
          },
          credentials: 'include'
        })
        if (response.ok) {
          this.user = null
          this.isAuthenticated = false
          this.saveState()
          if (router){
            await router.push({name: "login"})
          }
        }
      } catch (error) {
        console.error('Logout failed', error)
        throw error
      }
    },

    async fetchUser() {
      try {
        const response = await fetch('http://localhost:8000/api/user', {
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
          },
        })
        if (response.ok) {
          const data = await response.json()
          this.user = data
          this.isAuthenticated = true
        }
        else{
          this.user = null
          this.isAuthenticated = false
        }
      } catch (error) {
        console.error('Failed to fetch user', error)
        this.user = null
        this.isAuthenticated = false
      }
      this.saveState()
    },

    saveState() {
      /*
      We save state to local storage to keep the
      state when the user reloads the page.

       */
      localStorage.setItem('authState', JSON.stringify({
        user: this.user,
        isAuthenticated: this.isAuthenticated
      }))
    }
  }
})

export function getCSRFToken() {
  /*
  We get the CSRF token from the cookie to include in our requests.
  This is necessary for CSRF protection in Django.
   */
  const name = 'csrftoken';
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  if (cookieValue === null) {
    throw new Error('Missing CSRF cookie.')
  }
  return cookieValue;
}
