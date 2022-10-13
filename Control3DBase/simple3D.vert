attribute vec3 a_position;
attribute vec3 a_normal;

uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

//uniform vec4 u_color;
uniform vec4 u_light_position;
uniform vec4 u_light_diffuse;
uniform vec4 u_light_ambient;
uniform vec4 u_light_specular;

uniform vec4 u_material_diffuse;
uniform vec4 u_material_ambient;
uniform vec4 u_material_specular;
uniform vec4 u_material_shiny;

uniform vec4 u_eye_position;


varying vec4 v_color;  //Leave the varying variables alone to begin with

void main(void)
{
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);
	vec4 s = vec4(0);
	vec4 v = vec4(0);
	vec4 h = vec4(0);
	float lambert = 0.0;
	float phong = 0.0;

	position = u_model_matrix * position;
	normal = u_model_matrix * normal;
	
	s = u_light_position-position;
	lambert = max(0.0,dot(normal, s)/(normal.length()*s.length()));
	
	v = u_eye_position-position;
	h = (s+v)*0.5
	phong =  max(0.0,dot(normal, h)/(normal.length()*h.length()));

	//old lighting
	//float light_factor_1 = max(dot(normalize(normal), normalize(vec4(1, 2, 3, 0))), 0.0); 
	//float light_factor_2 = max(dot(normalize(normal), normalize(vec4(-3, -2, -1, 0))), 0.0);
	//v_color = (light_factor_1 + light_factor_2) * u_color; // ### --- Change this vector (pure white) to color variable --- #####


	v_color = u_light_ambient * u_material_ambient + lambert * u_light_diffuse * u_material_diffuse + u_light_specular * u_material_specular * pow(phong,u_material_shiny);

	position = u_view_matrix * position;
	position = u_projection_matrix * position;

	gl_Position = position;
}