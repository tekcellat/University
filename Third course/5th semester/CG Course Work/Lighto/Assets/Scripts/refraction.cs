using UnityEngine;
using System.Collections;

public class refraction : MonoBehaviour {

    public int rotationconstant = 1;
	// Use this for initialization
	void Start () {
	
	}
	
	// Update is called once per frame
	void Update () {
	
	}
    void OnTriggerEnter2D(Collider2D other)
    {
        other.gameObject.transform.Rotate(0, 0, - rotationconstant * Mathf.Cos(this.transform.rotation.eulerAngles.z * Mathf.Deg2Rad));
    }
}
