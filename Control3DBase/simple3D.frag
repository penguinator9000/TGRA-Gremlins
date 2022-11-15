//varying vec4 v_color;
uniform vec4 u_global_ambiance;

uniform sampler2D u_tex01;
uniform sampler2D u_tex02;

uniform vec4 u_light_diffuse[10];
uniform vec4 u_light_ambient[10];
uniform vec4 u_light_specular[10];
uniform float u_light_reach[10];

uniform float u_light_count_frag;

uniform vec4 u_material_diffuse;
uniform vec4 u_material_ambient;
uniform vec4 u_material_specular;
uniform float u_material_shiny;

varying vec4 v_normal[10];
varying vec4 v_s[10];
varying vec4 v_h[10];
varying vec2 v_uv;

void main(void)
{
    vec4 mat_tex = texture2D(u_tex01,v_uv);
    vec4 spe_tex = texture2D(u_tex02,v_uv);
    //Light 1
    vec4 light = vec4(0);

    for(int i = 0 ; i<u_light_count_frag;i++){
        float light_intesity =1.0;
        if (u_light_reach[i] != 0){
            float distance = length(v_s[i]);
            if( distance > u_light_reach[i]){
                light_intesity = 0;
            }
            else {
                light_intesity =1- distance/ u_light_reach[i];
            }
        }

        float lambert = 0.0;
        float phong = 0.0;

        lambert = max(0.0,dot(v_normal[i], v_s[i])/(length(v_normal[i])*length(v_s[i])));

        phong =  max(0.0,dot(normalize(v_normal[i]), normalize(v_h[i])));

        phong = pow(phong, u_material_shiny);

        light = light+(u_light_ambient[i] * u_material_ambient * mat_tex + lambert * u_light_diffuse[i] * u_material_diffuse * mat_tex + u_light_specular[i] * u_material_specular * spe_tex * phong)* light_intesity;
    }
    
    //all together
	//vec4 all_together;
    gl_FragColor = u_global_ambiance*u_material_ambient * mat_tex + light;
    //gl_FragColor = all_together * mat_tex;
}