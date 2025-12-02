(function() {
  'use strict';

  // Auto-run when script loads
  console.log('[Pulse Retention Widget] Initializing...');

  // Read attributes from the script tag with robust fallbacks
  function readWidgetAttributes() {
    // Primary: document.currentScript (works when script is executed inline or immediately after being added)
    const cs = document.currentScript;
    if (cs) {
      const b = cs.getAttribute('data-business-id');
      const e = cs.getAttribute('data-email');
      if (b || e) return { businessId: b || 'UNKNOWN', customerEmail: e || 'UNKNOWN' };
    }

    // Fallback: find any script tag whose src contains the widget filename
    try {
      const scripts = Array.from(document.getElementsByTagName('script'));
      for (let i = scripts.length - 1; i >= 0; i--) {
        const s = scripts[i];
        const src = s.getAttribute('src') || '';
        if (src.indexOf('pulse-retention-widget.js') !== -1) {
          const b = s.getAttribute('data-business-id');
          const e = s.getAttribute('data-email');
          if (b || e) return { businessId: b || 'UNKNOWN', customerEmail: e || 'UNKNOWN' };
        }
      }
    } catch (err) {
      console.warn('[Pulse Retention Widget] Fallback script scan failed', err);
    }

    // Final fallback: a global host variable (host page can set window.__PULSE_WIDGET_DATA__ = {businessId, email})
    try {
      if (window.__PULSE_WIDGET_DATA__) {
        const d = window.__PULSE_WIDGET_DATA__;
        return { businessId: d.businessId || 'UNKNOWN', customerEmail: d.email || 'UNKNOWN' };
      }
    } catch (err) {
      // ignore
    }

    // Default unknowns
    return { businessId: 'UNKNOWN', customerEmail: 'UNKNOWN' };
  }

  const attrs = readWidgetAttributes();
  const businessId = attrs.businessId;
  const customerEmail = attrs.customerEmail;

  console.log('[Pulse Retention Widget] Business ID:', businessId);
  console.log('[Pulse Retention Widget] Customer Email:', customerEmail);

  // Extract customer's first name from email
  function getCustomerName(email) {
    if (!email || email === 'UNKNOWN') return 'Valued Customer';
    const localPart = email.split('@')[0];
    // Capitalize first letter
    const name = localPart.charAt(0).toUpperCase() + localPart.slice(1);
    return name;
  }

  const customerName = getCustomerName(customerEmail);

  // Dummy data for now (personalized)
  const dummyPopupData = {
    title: `Hello ${customerName}!`,
    message: `
      <p><strong>We have exclusive offers just for you!!</strong></p>
      <ul>
        <li>🚗 Get <strong>₹200 OFF</strong> on your next ride</li>
        <li>🍕 <strong>50% OFF</strong> on food delivery (up to ₹150)</li>
        <li>📦 <strong>FREE delivery</strong> on your next grocery order</li>
      </ul>
      <p>As you are our special customer, these offers are exclusively for you!</p>
    `,
    cta_text: "Claim Your Offer",
    cta_link: "#"
  };

  // Backend call (commented out for now)
  // function fetchPopupData() {
  //   return fetch(`/api/popup?business_id=${businessId}&email=${encodeURIComponent(customerEmail)}`)
  //     .then(response => response.json())
  //     .then(data => {
  //       console.log('[Pulse Retention Widget] Fetched popup data:', data);
  //       return data;
  //     })
  //     .catch(error => {
  //       console.error('[Pulse Retention Widget] Error fetching popup data:', error);
  //       return null;
  //     });
  // }

  // Log popup event to backend (commented out for now)
  function logPopupEvent(eventType, eventData = {}) {
    console.log('[Pulse Retention Widget] Event:', eventType, eventData);

    // Backend event logging
    // fetch('/api/popup-event', {
    //   method: 'POST',
    //   headers: {
    //     'Content-Type': 'application/json'
    //   },
    //   body: JSON.stringify({
    //     business_id: businessId,
    //     customer_email: customerEmail,
    //     event_type: eventType,
    //     event_data: eventData,
    //     timestamp: new Date().toISOString()
    //   })
    // })
    // .then(response => response.json())
    // .then(data => {
    //   console.log('[Pulse Retention Widget] Event logged:', data);
    // })
    // .catch(error => {
    //   console.error('[Pulse Retention Widget] Error logging event:', error);
    // });
  }

  // Render the popup
  function renderPopup(popupData) {
    // Check if popup already exists
    if (document.getElementById('pulse-retention-popup')) {
      console.log('[Pulse Retention Widget] Popup already exists, skipping render');
      return;
    }

    // Create popup HTML
    const popupHTML = `
      <div id="pulse-retention-popup" class="pulse-popup-overlay">
        <div class="pulse-popup-container">
          <button class="pulse-popup-close" id="pulse-popup-close-btn">&times;</button>
          <div class="pulse-popup-header">
            <h2 class="pulse-popup-title">${popupData.title}</h2>
          </div>
          <div class="pulse-popup-body">
            <div class="pulse-popup-message">${popupData.message}</div>
          </div>
          <div class="pulse-popup-footer">
            <a href="${popupData.cta_link}" class="pulse-popup-cta" id="pulse-popup-cta-btn">
              ${popupData.cta_text}
            </a>
          </div>
        </div>
      </div>
    `;

    // Inject popup into the page
    document.body.insertAdjacentHTML('beforeend', popupHTML);
    console.log('[Pulse Retention Widget] Popup rendered');

    // Log popup shown event
    logPopupEvent('popup_shown', { title: popupData.title });

    // Add event listeners
    const closeBtn = document.getElementById('pulse-popup-close-btn');
    const ctaBtn = document.getElementById('pulse-popup-cta-btn');
    const overlay = document.getElementById('pulse-retention-popup');

    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        closePopup();
        logPopupEvent('popup_closed', { action: 'close_button' });
      });
    }

    if (ctaBtn) {
      ctaBtn.addEventListener('click', () => {
        logPopupEvent('popup_cta_clicked', { cta_text: popupData.cta_text, cta_link: popupData.cta_link });
      });
    }

    if (overlay) {
      overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
          closePopup();
          logPopupEvent('popup_closed', { action: 'overlay_click' });
        }
      });
    }
  }

  // Close the popup
  function closePopup() {
    const popup = document.getElementById('pulse-retention-popup');
    if (popup) {
      popup.style.opacity = '0';
      setTimeout(() => {
        popup.remove();
        console.log('[Pulse Retention Widget] Popup closed and removed');
      }, 300);
    }
  }

  // Initialize the widget with delay
  function initWidget() {
    // Use dummy data for now
    const popupData = dummyPopupData;

    // To use backend data in the future:
    // fetchPopupData().then(data => {
    //   if (data) {
    //     renderPopup(data);
    //   } else {
    //     console.log('[Pulse Retention Widget] No popup data available');
    //   }
    // });

    // Shorter delay for testing; change back to 2500ms in production if desired
    const delayMs = 800; // 800ms
    setTimeout(() => {
      renderPopup(popupData);
    }, delayMs);

    console.log(`[Pulse Retention Widget] Popup will appear in ${delayMs}ms`);
  }

  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initWidget);
  } else {
    initWidget();
  }

})();
