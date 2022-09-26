import httpRequest from "@/request";

interface DelUserParam extends POST_METHOD{
    id:string
}

interface DelComplaintParam extends POST_METHOD{
    id:string
}

interface DelMaintainParam extends POST_METHOD{
    id:string
}

interface DelChargeParam extends POST_METHOD{
    id:string
}

interface DelAnnouncementParam extends POST_METHOD{
    id:string
}

export function apiDelUser(param:DelUserParam){
     return httpRequest({
		url: '/del_data/user',
		method: 'post',
		data:param
	})
}

export function apiDelComplaint(param:DelComplaintParam){
     return httpRequest({
		url: '/del_data/complaint',
		method: 'post',
		data:param
	})
}

export function apiDelMaintain(param:DelMaintainParam){
     return httpRequest({
		url: '/del_data/maintain',
		method: 'post',
		data:param
	})
}

export function apiDelCharge(param:DelChargeParam){
     return httpRequest({
		url: '/del_data/charge',
		method: 'post',
		data:param
	})
}

export function apiDelAnnouncement(param:DelAnnouncementParam){
     return httpRequest({
		url: '/del_data/announcement',
		method: 'post',
		data:param
	})
}
