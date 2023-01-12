package projectC.repository;


import DTO.Client;


public interface ClientRepository {
	Client findByClientId(String clientId);

}
