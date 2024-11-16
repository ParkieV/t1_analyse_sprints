import { DateSelectorComponent } from "../../../components/date-selector/date-selector.component";

import { Component } from '@angular/core';
@Component({
  selector: 'app-home-filters',
  standalone: true,
  imports: [DateSelectorComponent],
  templateUrl: './home-filters.component.html',
  styleUrl: './home-filters.component.scss'
})
export class HomeFiltersComponent {

}
