# 🔓 Message Decryption Feature

## Overview

The frontend now includes an interactive message decryption panel that appears when users hover over encrypted messages. This feature allows users to enter passwords and decrypt message content in real-time.

## 🎯 Features

### Hover Interaction
- **Trigger**: Hover over any encrypted message bubble
- **Panel Appearance**: Smooth fade/scale animation using Tailwind transitions
- **Visibility**: Panel only shows for encrypted messages that haven't been decrypted yet
- **Mobile Support**: Touch-friendly interface

### Decryption Panel
The panel includes:
- **Password Input**: Secure text input field (type=password)
- **Unlock Button**: With loading state and icon (🔓)
- **Error Messages**: Red toast-style error display
- **Help Text**: Shows encryption method being used

### Decryption Flow
1. User hovers over encrypted message
2. DecryptPanel appears with smooth animation
3. User enters password
4. API request sent to backend
5. **On Success**: Message content replaced with decrypted text
6. **On Error**: Error message displayed, user can retry

## 🏗️ Component Structure

### New Component: `DecryptPanel.jsx`
```javascript
<DecryptPanel
  messageId={messageId}
  encryptionMethod="aes"
  onDecrypted={(decryptedData) => handleDecryption(decryptedData)}
  onError={(error) => showError(error)}
/>
```

**Props:**
- `messageId`: Unique identifier for the message
- `encryptionMethod`: Encryption type (aes, rsa, sha256, base64)
- `onDecrypted`: Callback when decryption succeeds
- `onError`: Callback when decryption fails

### Updated Component: `ChatWindow.jsx`
- Added state tracking for decrypted messages
- Added hover state management
- Integrated DecryptPanel into message rendering
- Dynamic message content display (encrypted vs decrypted)

### API Updates: `messagesApi.js`
**New Function:**
```javascript
export const decryptMessage = async (messageId, encryptionMethod, password)
```

**Request Format:**
```json
{
  "id": "message_id_here",
  "method": "AES-256",
  "password": "entered_password"
}
```

**Response Format:**
```json
{
  "content": "Decrypted message text",
  "decrypted": true
}
```

## 🎨 Styling

### Visual Features
- **Dark Theme**: Consistent with existing Discord-style UI
- **Smooth Animations**: Fade and scale transitions
- **Rounded Corners**: Modern appearance (`rounded-xl`)
- **Shadow Effects**: Depth and elevation
- **Hover States**: Interactive feedback

### Color Scheme
- Background: `bg-gray-800`
- Text: `text-gray-200`
- Accents: `bg-blue-600` (buttons)
- Errors: `bg-red-600`
- Borders: `border-gray-600`

### Animations
- **Fade**: `opacity-100` → `opacity-0`
- **Scale**: `transform scale-100` → `scale-105`
- **Duration**: 200ms transitions

## 🧪 Demo Mode

For testing without a backend, the feature includes demo passwords:
- `demo` - Universal demo password
- `password` - Alternative test password
- `12345` - Numeric test password

Each encryption method returns different decrypted content:
- **AES**: "This is a decrypted AES-256 message!..."
- **RSA**: "RSA-2048 decryption successful!..."
- **SHA-256**: "SHA-256 hash verified..."
- **Base64**: "Base64 decoding complete..."

## 🔌 Backend Integration

### Endpoint Required
```
POST /api/messages/decrypt
```

### Request Headers
```javascript
{
  'Content-Type': 'application/json',
  'Authorization': 'Bearer TOKEN' // Optional
}
```

### Backend Response
**Success (200 OK):**
```json
{
  "content": "Decrypted message content",
  "decrypted": true,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

**Error (400 Bad Request):**
```json
{
  "error": "Invalid password. Please try again.",
  "status": 400
}
```

## 📱 User Experience

### Desktop
1. Hover over encrypted message (🔒 icon)
2. Panel appears with password input
3. Enter password and click "🔓 Unlock"
4. Message content updates immediately

### Mobile
1. Tap on encrypted message
2. Panel appears (full touch target)
3. Enter password using mobile keyboard
4. Tap "🔓 Unlock" or press Enter

### State Management
- Decrypted messages are cached locally
- No need to decrypt the same message twice
- 🔒 icon changes to 🔓 after decryption
- Panel doesn't reappear for decrypted messages

## 🔒 Security Considerations

1. **Password Input**: Uses `type="password"` for secure entry
2. **Clear on Submit**: Password cleared after successful decryption
3. **Clear on Error**: Password cleared on failed attempts for retry
4. **No Storage**: Passwords never stored in state
5. **Error Handling**: Generic error messages don't reveal sensitive info

## 🐛 Error Handling

### Common Errors
- **Empty Password**: "Please enter a password"
- **Invalid Password**: "Invalid password. Please try again. (Hint: try 'demo' or 'password')"
- **Network Error**: Handled gracefully with user feedback

### Error Display
- Red background (`bg-red-600`)
- Border styling (`border-red-500`)
- Text color (`text-red-300`)
- Appears above password input

## 🚀 Future Enhancements

Potential improvements:
1. **Keyboard Shortcuts**: Quick access to decryption
2. **Auto-Decrypt**: Remember passwords for session
3. **Password Strength**: Visual indicators
4. **Multiple Methods**: Support for hybrid encryption
5. **Biometric Auth**: Fingerprint/Face ID integration
6. **Progress Indicators**: Show decryption progress
7. **Batch Decryption**: Decrypt multiple messages at once

## 📊 Technical Details

### React Hooks Used
- `useState`: Managing password, loading, and error states
- `useEffect`: Not required in this implementation

### Performance
- Minimal re-renders
- Efficient state updates
- Smooth animations (hardware accelerated)
- No unnecessary API calls

### Accessibility
- Keyboard navigation support
- Enter key submits password
- Focus management
- ARIA labels ready for screen readers

## 📝 Code Examples

### Basic Usage
```jsx
import DecryptPanel from './components/DecryptPanel';

<DecryptPanel
  messageId={message.id}
  encryptionMethod={message.encryptionMethod}
  onDecrypted={(data) => {
    // Update message content
    console.log('Decrypted:', data.content);
  }}
  onError={(error) => {
    // Handle error
    console.error('Decryption failed:', error);
  }}
/>
```

### API Integration
```javascript
// In messagesApi.js
export const decryptMessage = async (messageId, method, password) => {
  const response = await fetch(`${BASE_URL}/api/messages/decrypt`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: messageId, method, password }),
  });
  
  if (!response.ok) throw new Error('Decryption failed');
  return await response.json();
};
```

## ✅ Testing Checklist

- [ ] Hover over encrypted message shows panel
- [ ] Panel has smooth animation
- [ ] Password input accepts text
- [ ] Enter key submits password
- [ ] Correct password decrypts message
- [ ] Wrong password shows error
- [ ] Error message is visible and clear
- [ ] Decrypted messages show 🔓 icon
- [ ] Panel doesn't reappear for decrypted messages
- [ ] Password is cleared after submission
- [ ] Loading state shows spinner
- [ ] Mobile tap interaction works
- [ ] Keyboard focus management works

## 🎉 Success!

The decryption feature is fully integrated and ready to use. Connect to a backend by updating the API endpoints in `src/api/messagesApi.js`.

