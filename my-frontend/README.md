# Secure Chat Frontend - React + TailwindCSS

A modern, responsive chat application built with React and TailwindCSS, featuring encryption method selection and real-time messaging capabilities.

## 📁 Project Structure

```
src/
 ├─ components/
 │   ├─ Sidebar.jsx            → Encryption methods section
 │   ├─ ChatWindow.jsx         → Displays all messages (GET)
 │   ├─ MessageInput.jsx       → Input field + Send button (POST)
 │   └─ PasswordStatus.jsx     → Top-right password status indicator
 ├─ api/
 │   └─ messagesApi.js         → Contains GET, POST, DELETE API calls
 ├─ App.jsx                    → Main layout combining all components
 ├─ index.css                  → Tailwind base styles
 └─ main.jsx                   → React entry point
```

## 🎨 Features

- **Dark Theme**: Beautiful dark grey theme (#1e1e1e → #2a2a2a)
- **Encryption Methods**: Sidebar with multiple encryption options (AES, RSA, SHA256, Base64)
- **Chat Interface**: Discord-style message bubbles
- **Password Status**: Visual indicator for lock/unlock status
- **Responsive Design**: Works on desktop and tablet
- **Smooth Animations**: Transitions and hover effects

## 🚀 Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Navigate to the frontend directory:
```bash
cd my-frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The app will open at `http://localhost:3000`

## 🛠️ Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

## 🔌 API Integration

The project includes placeholder API calls in `src/api/messagesApi.js`. To connect to your backend:

1. Update the `BASE_URL` constant in `src/api/messagesApi.js`
2. Ensure your backend provides the following endpoints:
   - `GET /api/messages` - Fetch all messages
   - `POST /api/messages` - Create a new message
   - `DELETE /api/messages/:id` - Delete a message

## 📦 Dependencies

- React 19.2.0
- React DOM 19.2.0
- TailwindCSS 3.4.1
- Autoprefixer 10.4.16
- PostCSS 8.4.32

## 🎨 Styling

- **Font**: Inter (Google Fonts)
- **Colors**: Dark grey palette with blue accents
- **Utilities**: Tailwind CSS with custom utilities
- **Animations**: Custom animations for message bubbles

## 🔐 Encryption Methods

The sidebar supports the following encryption methods:
- **No Encryption** - Send unencrypted messages
- **AES-256** - Advanced Encryption Standard
- **RSA-2048** - Rivest-Shamir-Adleman
- **SHA-256** - Secure Hash Algorithm
- **Base64** - Base64 encoding

## 📝 Components

### Sidebar.jsx
- Vertical layout with encryption method buttons
- Active state highlighting
- Hover effects

### ChatWindow.jsx
- Fetches messages on load
- Auto-scrolls to bottom
- Loading and error states
- Message bubble styling

### MessageInput.jsx
- Controlled input component
- Send button with loading state
- Encryption method indicator
- Enter key support

### PasswordStatus.jsx
- Top-right floating indicator
- Lock/unlock visualization
- Expandable details panel

## 🚧 Development Status

The frontend is fully functional with dummy data. To connect to a backend:
1. Implement the API endpoints in `messagesApi.js`
2. Add authentication if needed
3. Update the BASE_URL constant

## 📄 License

This project is licensed under the MIT License.
