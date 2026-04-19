import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-register-page',
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
    <section class="panel auth">
      <div>
        <p class="eyebrow">Student Registration</p>
        <h1>Create your account</h1>
        <p class="description">Sign up once and start creating subject-based study groups right away.</p>
      </div>

      <form class="form" (ngSubmit)="register()">
        <label>
          Username
          <input [(ngModel)]="username" name="username" type="text" required />
        </label>

        <label>
          Password
          <input [(ngModel)]="password" name="password" type="password" minlength="8" required />
        </label>

        <label>
          Confirm password
          <input [(ngModel)]="confirmPassword" name="confirmPassword" type="password" minlength="8" required />
        </label>

        @if (errorMessage) {
          <p class="error">{{ errorMessage }}</p>
        }

        <div class="actions">
          <button type="submit" [disabled]="isSubmitting">
            {{ isSubmitting ? 'Creating account...' : 'Register' }}
          </button>
          <a routerLink="/login" class="link-button">Back to login</a>
        </div>
      </form>
    </section>
  `,
  styles: [`
    .panel {
      max-width: 42rem;
      margin: 4rem auto;
      padding: 2rem;
      border-radius: 24px;
      background: rgba(255,255,255,.82);
      border: 1px solid rgba(20,48,79,.12);
      box-shadow: 0 18px 40px rgba(20,48,79,.08);
    }
    .auth { display: grid; gap: 1.5rem; }
    .eyebrow { margin: 0 0 .75rem; color: #b14e19; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; }
    h1 { margin: 0 0 .5rem; font-size: clamp(2rem, 6vw, 3rem); }
    .description { margin: 0; color: #5a6a7f; line-height: 1.6; }
    .form { display: grid; gap: 1rem; }
    label { display: grid; gap: .45rem; font-weight: 600; color: #14304f; }
    input {
      border-radius: 16px; border: 1px solid rgba(20,48,79,.14); padding: .95rem 1rem;
      font: inherit; background: #fff;
    }
    .actions { display: flex; gap: .75rem; flex-wrap: wrap; align-items: center; }
    button, .link-button {
      justify-self: start; border: 0; border-radius: 999px; padding: .9rem 1.4rem;
      background: #da6b2d; color: #fff; font-weight: 700; cursor: pointer; text-decoration: none;
    }
    .link-button { background: #fff; color: #14304f; border: 1px solid rgba(20,48,79,.12); }
    .error { margin: 0; color: #b42318; font-weight: 600; }
  `]
})
export class RegisterPageComponent {
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);

  protected username = '';
  protected password = '';
  protected confirmPassword = '';
  protected errorMessage = '';
  protected isSubmitting = false;

  protected register(): void {
    this.errorMessage = '';

    if (this.password !== this.confirmPassword) {
      this.errorMessage = 'Passwords do not match.';
      return;
    }

    this.isSubmitting = true;
    this.authService
      .register({
        username: this.username,
        password: this.password,
        confirm_password: this.confirmPassword
      })
      .subscribe({
        next: () => {
          this.isSubmitting = false;
          this.router.navigate(['/groups']);
        },
        error: (error) => {
          this.isSubmitting = false;
          this.errorMessage = error?.error?.error ?? error?.error?.username?.[0] ?? 'Registration failed.';
        }
      });
  }
}
