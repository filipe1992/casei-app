import React from 'react'
import { createRoot } from 'react-dom/client'
import { ThemeProvider } from '@material-tailwind/react'
import './index.css'
import App from './App.jsx'

const root = createRoot(document.getElementById('root'))

root.render(
  <ThemeProvider>
    <App />
  </ThemeProvider>
)
