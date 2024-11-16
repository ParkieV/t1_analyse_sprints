import { Component } from '@angular/core';
import { MatSelectModule } from '@angular/material/select';
import { Company } from '../../models/company.model';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatMenuModule } from '@angular/material/menu';
import { AuthService } from '../../services/auth.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatFormFieldModule,
    MatSelectModule,
    MatMenuModule,
  ],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss',
})
export class HeaderComponent {
  isProfileLoading = false;

  constructor(public readonly authService: AuthService) {}

  companies: Company[] = [
    {
      id: '1',
      name: 'Компания Т1',
    },
  ];

  company!: Company;

  ngOnInit() {
    this.company = this.companies[0];
  }

  signIn() {
    this.isProfileLoading = true;
    return this.authService.signIn('User', 'Qwerty123.').subscribe((res) => {
      this.isProfileLoading = false;
    });
  }

  signOut() {
    this.isProfileLoading = true;
    return this.authService.signOut().subscribe(() => {
      this.isProfileLoading = false;
    });
  }
}
