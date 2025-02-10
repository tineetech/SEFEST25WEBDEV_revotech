
const LoadSnapScript = () => {
    return new Promise((resolve, reject) => {
        if (window.snap) {
            resolve(window.snap);
            return;
        }

        const script = document.createElement("script");
        script.src = "https://app.sandbox.midtrans.com/snap/snap.js";
        script.setAttribute("data-client-key", import.meta.env.CLIENT_KEY_MIDTRANS);
        script.onload = () => resolve(window.snap);
        script.onerror = (e) => reject(e);
        document.body.appendChild(script);
      });
  };

export default LoadSnapScript