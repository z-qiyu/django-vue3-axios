// 导入axios实例
import httpRequest from '@/request/index'

interface ComplaintParam extends POST_METHOD{
	msg: string
}

interface MaintainParam extends POST_METHOD{
	msg: string
}

interface ChargeParam extends POST_METHOD{
	type: string,
	money: number
}

interface AnnouncementParam extends POST_METHOD{
	title: string,
	content: string
}

interface UpdateMaintainParam extends POST_METHOD{
	id:string
}

export function apiPutComplaint(param:ComplaintParam){
    return httpRequest({
		url: '/complaint',
		method: 'put',
		data: param,
	})
}


export function apiPutMaintain(param:MaintainParam){
    return httpRequest({
		url: '/maintain',
		method: 'put',
		data: param,
	})
}

export function apiPutCharge(param:ChargeParam){
    return httpRequest({
		url: '/charge',
		method: 'put',
		data: param,
	})
}

export function apiPutAnnouncement(param:AnnouncementParam){
    return httpRequest({
		url: '/announcement',
		method: 'put',
		data: param,
	})
}

export function apiUpdateMaintain(param:UpdateMaintainParam){
    return httpRequest({
		url: '/updateMaintain',
		method: 'POST',
		data: param,
	})
}

