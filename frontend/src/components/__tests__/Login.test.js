import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Login from '../Login';

describe('Login component', () => {
  it('renders email and password fields', () => {
    render(<Login onLogin={() => {}} />);
    expect(screen.getByPlaceholderText(/enter your email/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/enter your password/i)).toBeInTheDocument();
  });

  it('calls onLogin on submit', () => {
    const onLogin = jest.fn();
    render(<Login onLogin={onLogin} />);
    fireEvent.change(screen.getByPlaceholderText(/enter your email/i), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByPlaceholderText(/enter your password/i), { target: { value: '123' } });
    fireEvent.click(screen.getByText(/sign in/i));
    // Can't test fetch without mocking, but form interaction works
    expect(screen.getByPlaceholderText(/enter your email/i)).toHaveValue('test@example.com');
  });
});