package projectC.repository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import DTO.Client;
import projectC.service.BusinessModel;

@Repository
public class ClientRepositoryImp implements ClientRepository{
	
	private BusinessModel bmodel;
	
	@Autowired
	public ClientRepositoryImp(BusinessModel bmodel) {
		this.bmodel = bmodel;
	}
	
	public Client findByClientId(String clientId) {
		return bmodel.getClientInfo(clientId);
	}

}
