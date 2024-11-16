import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { SidebarComponent } from './sidebar/sidebar.component';
import { HeaderComponent } from './header/header.component';
import { NgScrollbarModule } from 'ngx-scrollbar';
import { TranslateService } from '@ngx-translate/core';
import translationsRU from "../../public/i18n/ru.json";
import translationsEN from "../../public/i18n/en.json";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, SidebarComponent, HeaderComponent, NgScrollbarModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  constructor(private _translate: TranslateService) {
    this._translate.setTranslation('ru', translationsRU);
    this._translate.setTranslation('en', translationsEN);
    this._translate.addLangs(['ru', 'en']);
    this._translate.setDefaultLang('ru');
    this._translate.use('ru');
  }
}
