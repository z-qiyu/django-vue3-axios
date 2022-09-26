// 导入axios实例
import httpRequest from '@/request/index'

// 定义接口的传参
interface UserInfoParam extends POST_METHOD{
	username: string
}

// 定义接口的传参
interface UserInfosParam extends POST_METHOD {
	page: string
}

interface RegisterParam extends POST_METHOD{
    username: string,
	gender: string,
	user_type: boolean, // false 用户 ,true 维修员
	email:string,
	password: string,
	tel:number,
	re_password: string
}

interface LoginParam extends POST_METHOD{
    username: string,
	password: string,
}

interface DeleteUser extends POST_METHOD{
	password: string
}

interface AddPropertyParam  extends POST_METHOD{
	t: Array<string>
}


// 获取用户信息
export function apiGetUserInfo(param: UserInfoParam) {
    return httpRequest({
		url: '/user/getinfo',
		method: 'get',
		data: param
	})
}

// 获取一批用户信息
export function apiGetUserInfos(param: UserInfosParam) {
    return httpRequest({
		url: '/user/getinfos',
		method: 'post',
		data: param,
	})
}

// 注册
export function apiRegister(param: RegisterParam) {
    return httpRequest({
		url: '/user/register',
		method: 'post',
		data: param,
	})
}

// 登录
export function apiLogin(param: LoginParam) {
    return httpRequest({
		url: '/user/login',
		method: 'post',
		data: param,
	})
}

// 注销用户信息
export function apiDelete(param: DeleteUser) {
    return httpRequest({
		url: '/user/off',
		method: 'delete',
		data: param,
	})
}

export function apiAddProperty(param:AddPropertyParam){
	return httpRequest({
		url: '/user/add_property',
		method: 'post',
		data: param,
	})
}

