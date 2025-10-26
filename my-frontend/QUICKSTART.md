# Quick Start Guide

## 🚀 Installation & Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd my-frontend
   ```

2. **Install dependencies** (TailwindCSS, Autoprefixer, PostCSS):
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm start
   ```

4. **Open your browser**:
   The app will automatically open at `http://localhost:3000`

## ✅ What's Included

### Components (all in `src/components/`)
- ✅ **Sidebar.jsx** - Encryption methods selector (AES, RSA, SHA256, Base64)
- ✅ **ChatWindow.jsx** - Message display area with auto-scroll
- ✅ **MessageInput.jsx** - Input field with send button
- ✅ **PasswordStatus.jsx** - Lock/unlock status indicator (top-right)

### API Layer (`src/api/`)
- ✅ **messagesApi.js** - Ready-to-use API functions:
  - `getMessages()` - Fetch all messages
  - `postMessage()` - Send a new message
  - `deleteMessage()` - Delete a message
  - All functions include dummy data fallback for offline development

### Configuration
- ✅ **TailwindCSS** configured and ready
- ✅ **PostCSS** with Autoprefixer
- ✅ **Inter Font** from Google Fonts
- ✅ Dark theme with Discord-style UI

## 🎨 Features Already Implemented

1. **Dark Theme** - Grey palette (#1e1e1e → #2a2a2a)
2. **Encryption Selection** - 5 methods in sidebar
3. **Message Bubbles** - Discord-style with animations
4. **Auto-scroll** - Messages automatically scroll to bottom
5. **Loading States** - Spinners and error handling
6. **Responsive Design** - Works on desktop and tablet
7. **Smooth Animations** - Transitions and hover effects
8. **Password Status** - Visual lock/unlock indicator

## 🔌 Connecting to Backend

The API functions in `src/api/messagesApi.js` are ready to connect to your backend:

1. Update the `BASE_URL` constant (currently set to `http://localhost:3001`)
2. Remove or comment out the dummy data in the catch blocks
3. Add authentication headers if needed
4. Your backend should provide these endpoints:
   - `GET /api/messages` - Returns array of messages
   - `POST /api/messages` - Creates and returns a new message
   - `DELETE /api/messages/:id` - Deletes a message

## 📝 API Endpoint Specifications

### GET /api/messages
**Returns:**
```json
[
  {
    "id": 1,
    "content": "Hello world",
    "timestamp": "2024-01-01T12:00:00Z",
    "sender": "User1",
    "encrypted": true,
    "encryptionMethod": "aes"
  }
]
```

### POST /api/messages
**Request Body:**
```json
{
  "content": "Your message",
  "encryptionMethod": "aes",
  "encrypted": true,
  "timestamp": "2024-01-01T12:00:00Z",
  "sender": "Current User"
}
```

**Returns:** Same as request body with `id` added

### DELETE /api/messages/:id
**Returns:** `true` on success

## 🎯 Current Behavior

With the dummy data, the app works offline:
- Shows 3 sample messages on load
- Can send new messages (stored in state, not persisted)
- All UI interactions work
- No backend connection required for development

## 🐛 Troubleshooting

### Tailwind not working?
- Make sure `tailwind.config.js` is in the root folder (not in `src/`)
- Run `npm install` to ensure dependencies are installed

### Port already in use?
- Change the port in `.env` file or command line:
  ```bash
  PORT=3001 npm start
  ```

### Module not found errors?
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again

## 📦 Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` folder.

