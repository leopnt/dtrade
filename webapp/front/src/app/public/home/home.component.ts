import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
    const links = document.querySelectorAll('a');

    links.forEach(function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        const href = link.getAttribute('href');
        const target = href ? document.querySelector(href) : null;
        if (target) {
          target.scrollIntoView({ behavior: 'smooth' });
        }
      });
    });
  }

}
