from app.app_cache.cache_access_layer import get_branch_details, cache_update, set_branch_details, get_bank, set_bank
from app.services.db_services import get_all_branches_details_service, get_bank_details_service
from app.utils import logger


def bank_branches_in_city_service(bank_name, city):

    # try cache first and return if cache hit
    result = get_branch_details(bank_name, city)
    if result:
        logger.info("from cache")
        return result

    logger.info("from db")
    # else db read and load to cache
    result = get_all_branches_details_service(bank_name, city)
    if len(result) == 0:  # if no branches found then return empty result
        return result

    # if some data found then start updating cache in background thread and return result
    cache_update(set_branch_details, bank_name, city, result)

    # return results
    return result


def bank_details_service(ifsc):

    # try cache first and return if cache hit
    result = get_bank(ifsc)
    if result:
        logger.info("from cache")
        return result

    logger.info("from db")
    # else db read and load to cache
    result = get_bank_details_service(ifsc)
    if len(result) == 0:
        return result

    # if some data found then start updating cache in background thread and return result
    cache_update(set_bank, ifsc, result)

    # return results
    return result
