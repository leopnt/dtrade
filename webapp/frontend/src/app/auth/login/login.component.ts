import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/_services/auth.service';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  form = {
    email: null,
    password_hash: null
  }

  server_error = false

  constructor(private http: HttpClient, private router: Router, private authService: AuthService) { }

  ngOnInit(): void {
  }

  onSubmit() {
    this.http.post('http://127.0.0.1:5000/api/v1/auth/login', this.form).subscribe(
      (response) => {
        // Traitement de la réponse
      },
      (err: HttpErrorResponse) => {
        console.log(err);
        if (err.status == 200) {
          this.authService.isLogged = true
          this.router.navigate(['sub'])
        } else {
          this.server_error = true;
        }
      }
    )
  }

}
