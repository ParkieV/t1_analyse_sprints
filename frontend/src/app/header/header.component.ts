import { Component } from '@angular/core';
import { MatSelectModule } from '@angular/material/select';
import { Company } from '../../models/company.model';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [FormsModule, MatFormFieldModule, MatSelectModule],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss',
})
export class HeaderComponent {
  companies: Company[] = [
    {
      id: 1,
      name: 'Компания Т1',
    },
    {
      id: 2,
      name: 'Компания Т1',
    },
    {
      id: 3,
      name: 'Компания Т1',
    },
  ];

  company?: Company;
}
