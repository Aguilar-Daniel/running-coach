function getCsrfToken() {
   const match = document.cookie.match(/(?:^|; )csrf_access_token=([^;]*)/);
   if (match) {return decodeURIComponent(match[1]); }
   return null;
}

async function apiRequest(method, path, body) {
   const options = {
      method: method, 
      headers: { 'Content-Type': 'application/json'},
   };

   if (['POST', 'PATCH', 'DELETE'].includes(method)) {
      options.headers['X-CSRF-TOKEN'] = getCsrfToken();
   }
   if (body !== undefined) {
      options.body = JSON.stringify(body);
   }

   const response = await fetch(`/api/v1${path}`, options); // ` ` used exactly like f strings
   let data;
   if (response.status === 204) {
      data = undefined;
   }
   else {
      data = await response.json();
   }   
   if (!response.ok) {
      let message;

      if (typeof data.error === "string" ) {
         message = data.error;
      }
      else if (typeof data.error === "object") {
         message = JSON.stringify(data.error);
      }
      else {
         message = JSON.stringify(data.errors) || 'request failed';
      }
      throw new Error(message);
   }

   return data;
}

async function requireAuth() {
   try {
      await apiRequest("GET", "/auth/me");
   } catch (err) {
      window.location.href = "/login.html";
   }
}

function showError(err) {
   const el = document.getElementById("error-message");
   el.textContent = err.message || String(err);
   el.hidden = false;
}