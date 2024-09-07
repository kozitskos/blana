"use client"

import axios from 'axios';


const API_BASE_URL = 'http://localhost:8000/notes';

// Helper to get the token from localStorage
const getToken = () => localStorage.getItem('token');

// Fetch all notes (GET /notes)
export const fetchNotes = async (skip = 0, limit = 10) => {
  const token = getToken();
  if (!token) throw new Error('No access token available');

  const response = await axios.get(API_BASE_URL, {
    headers: { Authorization: `Bearer ${token}` },
    params: { skip, limit },
  });

  return response.data;
};

// Fetch a single note by ID (GET /notes/{note_id})
export const fetchNoteById = async (noteId: string) => {
  const token = getToken();
  if (!token) throw new Error('No access token available');

  const response = await axios.get(`${API_BASE_URL}/${noteId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  return response.data;
};

// Create a new note (POST /notes)
export const createNote = async (noteData: { title: string; content: string }) => {
  const token = getToken();
  if (!token) throw new Error('No access token available');

  const response = await axios.post(
    API_BASE_URL,
    noteData,
    {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    }
  );

  return response.data;
};

// Update a note (PUT /notes/{note_id})
export const updateNote = async (noteId: string, noteData: { title: string; content: string }) => {
  const token = getToken();
  if (!token) throw new Error('No access token available');

  const response = await axios.put(
    `${API_BASE_URL}/${noteId}`,
    noteData,
    {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    }
  );

  return response.data;
};


// Delete a note (DELETE /notes/{note_id})
export const deleteNoteById = async (noteId: string) => {
  const token = getToken();
  if (!token) throw new Error('No access token available');

  const response = await axios.delete(`${API_BASE_URL}/${noteId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  return response.data;
};


export const patchNote = async (
  noteId: string,
  noteData: { title?: string; content?: string } // Both fields are optional
) => {
  const token = getToken();
  if (!token) throw new Error('No access token available');

  const response = await axios.patch(
    `${API_BASE_URL}/${noteId}`,
    noteData, // Send only the fields that are provided
    {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    }
  );

  return response.data;
};
