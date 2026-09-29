import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import App from './App';

describe('App Component', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('clicks the button and displays the movie title', async () => {

    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({
          title: 'Fake Vitest Movie',
          overview: 'Testing the UI works.',
          date: '2026-01-01',
        }),
      })
    );


    render(<App />);


    const button = screen.getByRole('button', { name: /get random movie/i });
    fireEvent.click(button);

    // 4. Verify title appears
    await waitFor(() => {
      expect(screen.getByText('Fake Vitest Movie')).toBeInTheDocument();
    });
  });
});