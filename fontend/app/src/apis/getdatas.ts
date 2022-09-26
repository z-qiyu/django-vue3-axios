// 导入axios实例
import httpRequest from '@/request/index'

interface PageInfosParam extends POST_METHOD{
    page: string
}

export function apiGetCarports(param: POST_METHOD){
    return httpRequest({
		url: '/get_data/carports',
		method: 'post',
		data: param,
	})
}

export function apiGetComplaintMessage(param: POST_METHOD){
    return httpRequest({
		url: '/get_data/complaintMessage',
		method: 'post',
		data: param,
	})
}

export function apiGetMaintainMessage(param: POST_METHOD){
    return httpRequest({
		url: '/get_data/maintainMessage',
		method: 'post',
		data: param,
	})
}
export function apiGetCharge(param: POST_METHOD){
    return httpRequest({
		url: '/get_data/charge',
		method: 'post',
		data: param,
	})
}
export function apiGetAnnouncement(param:POST_METHOD){
    return httpRequest({
		url: '/get_data/announcement',
		method: 'post',
		data:param
	})
}
