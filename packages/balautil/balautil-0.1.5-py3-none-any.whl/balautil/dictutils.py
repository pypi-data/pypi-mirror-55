import pandas as pd
def visite_every_key_value_in_dct(d, cond_f=None, path='d', values=[], debug=True, return_df=True):
    """
    d: dict/json like dict
    cond_f: function to check if the value is interesting or not
            example : to get all *.mp3
            cond_f = lambda x: x.endswith(".mp3")
            if cond_f is None, it will visit every key,value
    path: Optional: No need to pass this path
    debug=True: To print
    return_df=True: To return as df
    """
    if isinstance(d, dict):
        for k,v in d.items():
            if isinstance(v, str):
                if not cond_f:
                    if debug: print(v, path)
                    values.append((v, path))
                elif cond_f(v):
                    if debug: print(v, path)
                    values.append((v, path))

            if isinstance(v, (list,dict)):
                visite_every_key_value_in_dct(v, cond_f, path=str(path) +f'["{k}"]',values=values, debug=debug, return_df=return_df)
        
    if isinstance(d, list):
        for i, o in enumerate(d):
            visite_every_key_value_in_dct(o, cond_f,  path=str(path)+f"[{i}]", values=values, debug=debug, return_df=return_df)
    
    #return the final values list
    if return_df:
        return pd.DataFrame(values, columns=["val", "paths"])
    return values


def traverse_dct(d, f, **kwargs):
    """
    d: dict/json like dict
    cond_f: function to check if the value is interesting or not
            example : to get all *.mp3
            cond_f = lambda x: x.endswith(".mp3")
            if cond_f is None, it will visit every key,value
    path: Optional: No need to pass this path
    debug=True: To print
    return_df=True: To return as df
    """
    if not f: f = lambda x: True
    return visite_every_key_value_in_dct(d , f, values =[], **kwargs)