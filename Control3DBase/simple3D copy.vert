attribute vec4 a_position;
attribute vec4 a_normal;

uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;
uniform vec4 u_global_ambiance;

//uniform vec4 u_color;
uniform vec4 u_light_position;
uniform vec4 u_light_diffuse;
uniform vec4 u_light_ambient;
uniform vec4 u_light_specular;
uniform float u_light_reach;

uniform vec4 u_material_diffuse;
uniform vec4 u_material_ambient;
uniform vec4 u_material_specular;
uniform float u_material_shiny;


uniform float u_light2_reach;
uniform vec4 u_light2_position;
uniform vec4 u_light2_diffuse;
uniform vec4 u_light2_ambient;
uniform vec4 u_light2_specular;

uniform vec4 u_eye_position;


varying vec4 v_color;  //Leave the varying variables alone to begin with

void main(void)
{
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);
	
	vec4 light1 = vec4(0);

	position = u_model_matrix * position;
	normal = u_model_matrix * normal;

	vec4 v = u_eye_position - position;

	vec4 s = u_light_position - position;
	
	vec4 h = (s+v);
	float light_intesity =1.0;
	if (u_light_reach != 0){
		float distance = length(s);
		if( distance > u_light_reach){
			light_intesity = 0;
		}
		else {
			light_intesity = distance/ u_light_reach;
		}
	}


	float lambert = 0.0;
	float phong = 0.0;

	lambert = max(0.0,dot(normal, s)/(length(normal)*length(s)));

	phong =  max(0.0,dot(normalize(normal), normalize(h)));

	phong = pow(phong, u_material_shiny);

	light1 = (u_light_ambient * u_material_ambient + lambert * u_light_diffuse * u_material_diffuse + u_light_specular * u_material_specular * phong)* light_intesity;
	
	vec4 light2 = vec4(0);

	vec4 v2 = u_eye_position - position;

	vec4 s2 = u_light2_position - position;
	
	vec4 h2 = (s2+v2);
	float light2_intesity =1.0;
	if (u_light2_reach != 0){
		float distance2 = length(s2);
		if( distance2 > u_light2_reach){
			light2_intesity = 0;
		}
		else {
			light2_intesity = distance2/ u_light2_reach;
		}
	}

	float lambert2 = 0.0;
	float phong2 = 0.0;

	lambert2 = max(0.0,dot(normal, s2)/(length(normal)*length(s2)));

	phong2 =  max(0.0,dot(normalize(normal), normalize(h2)));

	phong2 = pow(phong2, u_material_shiny);

	light2 = (u_light2_ambient * u_material_ambient + lambert2 * u_light2_diffuse * u_material_diffuse + u_light2_specular * u_material_specular * phong2)* light2_intesity;


	v_color = u_global_ambiance*u_material_ambient + light1 + light2;
	
	position = u_view_matrix * position;
	position = u_projection_matrix * position;

	gl_Position = position;
}