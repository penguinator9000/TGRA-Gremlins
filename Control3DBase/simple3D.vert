attribute vec4 a_position;
attribute vec4 a_normal;
attribute vec2 a_uv;

uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;




//uniform vec4 u_color;
uniform vec4 u_light_position[10];


uniform float u_light2_reach;
uniform vec4 u_light2_position;
uniform vec4 u_light2_diffuse;
uniform vec4 u_light2_ambient;
uniform vec4 u_light2_specular;

uniform vec4 u_eye_position;


//varying vec4 v_color;  //Leave the varying variables alone to begin with

uniform float u_light_count_vert;

varying vec4 v_normal[10];
varying vec4 v_s [10];
varying vec4 v_h[10];
varying vec2 v_uv;

void main(void)
{
	
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);
	vec4 normal_arr[10];
	vec4 s_arr[10];  
	vec4 h_arr[10];
	position = u_model_matrix * position;
	
	//UV coords
	v_uv = a_uv;
	
	for(int i=0 ; i<u_light_count_vert;i++){
		
		normal_arr[i] = u_model_matrix * normal;

		vec4 v = u_eye_position - position;

		s_arr[i] = u_light_position[i] - position;

		h_arr[i] = (s_arr[i]+v);
	}
	v_normal = normal_arr;
	v_s = s_arr;
	v_h = h_arr;
	
	position = u_view_matrix * position;
	position = u_projection_matrix * position;

	gl_Position = position;
}