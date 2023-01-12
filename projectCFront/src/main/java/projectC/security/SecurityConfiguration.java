package projectC.security;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityCustomizer;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;

import projectC.repository.ClientRepositoryImp;
import projectC.service.BusinessModel;
import projectC.service.ClientRepositoryDetailsService;



@EnableWebSecurity
@Configuration
public class SecurityConfiguration{
		
	
	    @Bean
	    public PasswordEncoder passwordEncoder() {
	        return new BCryptPasswordEncoder();
	    }
	  
	
	 	@Bean
		public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
	 		
		    http
		    .authorizeHttpRequests()
		    .requestMatchers("/repository")
		    .authenticated()
		    .requestMatchers("/","/**")
		    .permitAll()
		    .and()
		    .formLogin()
		    .loginPage("/signin")
		    .loginProcessingUrl("/log/in")
		    .usernameParameter("username")
	        .passwordParameter("password")
	        .defaultSuccessUrl("/log/in")
		    .and()
		    .logout()
		    .logoutUrl("/log/out")
		    .logoutSuccessUrl("/log/out");
		        
		    return http.build();
		}
	 	
	 	
}
