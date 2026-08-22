import { render, screen } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

describe('Dayflow app', () => {
  beforeEach(() => {
    const storage = { getItem: () => null, setItem: vi.fn(), removeItem: vi.fn(), clear: vi.fn() };
    vi.stubGlobal('localStorage', storage);
    Object.defineProperty(window, 'localStorage', { value: storage, configurable: true });
  });

  it('renders the sign-in workspace for a fresh session', async () => {
    const { default: App } = await import('./App');
    render(<App />);
    expect(screen.getByText('Make work')).toBeTruthy();
    expect(screen.getByRole('button', { name: /enter HR workspace/i })).toBeTruthy();
  });
});